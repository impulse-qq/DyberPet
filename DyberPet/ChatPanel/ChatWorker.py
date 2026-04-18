from PySide6.QtCore import QRunnable, Signal, QObject
import httpx


class ChatWorkerSignals(QObject):
    response_received = Signal(str)
    error_occurred = Signal(str)


class ChatWorker(QRunnable):
    
    def __init__(self, messages, api_url, model_name, api_key=""):
        super().__init__()
        self.messages = messages
        self.api_url = api_url
        self.model_name = model_name
        self.api_key = api_key
        self.signals = ChatWorkerSignals()
    
    def run(self):
        try:
            headers = {}
            if self.api_key:
                key = self.api_key.strip()
                if key.lower().startswith("bearer "):
                    key = key[7:]
                headers["Authorization"] = f"Bearer {key}"
            with httpx.Client(timeout=30.0) as client:
                url = f"{self.api_url}chat/completions"
                payload = {
                    "model": self.model_name,
                    "messages": self.messages,
                    "stream": False
                }
                response = client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                self.signals.response_received.emit(content)
                
        except httpx.ConnectError as e:
            error_msg = f"Connection error: Unable to reach API at {self.api_url}"
            self.signals.error_occurred.emit(error_msg)
            
        except httpx.TimeoutException:
            error_msg = "Request timed out after 30 seconds"
            self.signals.error_occurred.emit(error_msg)
            
        except httpx.HTTPStatusError as e:
            error_msg = f"HTTP error {e.response.status_code}: {e.response.text}"
            self.signals.error_occurred.emit(error_msg)
            
        except (KeyError, IndexError) as e:
            error_msg = f"Invalid response format: {str(e)}"
            self.signals.error_occurred.emit(error_msg)
            
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.signals.error_occurred.emit(error_msg)

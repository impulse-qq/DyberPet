"""
ChatWorker module for LLM API calls.

Uses QRunnable + QThreadPool pattern for non-blocking API requests.
"""
from PySide6.QtCore import QRunnable, Signal, QObject
import httpx


class ChatWorkerSignals(QObject):
    """Signals for ChatWorker to communicate with main thread."""
    response_received = Signal(str)
    error_occurred = Signal(str)


class ChatWorker(QRunnable):
    """
    QRunnable worker for making LLM API calls.
    
    Runs in thread pool to avoid blocking main UI thread.
    Uses httpx for HTTP requests (lighter than OpenAI SDK).
    """
    
    def __init__(self, messages, api_url, model_name):
        """
        Initialize ChatWorker with API parameters.
        
        Args:
            messages: List of message dicts [{"role": "user", "content": "..."}]
            api_url: Base URL for API (e.g., "http://localhost:1234/v1/")
            model_name: Model identifier (e.g., "gpt-3.5-turbo")
        """
        super().__init__()
        self.messages = messages
        self.api_url = api_url
        self.model_name = model_name
        self.signals = ChatWorkerSignals()
    
    def run(self):
        """
        Execute API call in thread pool.
        
        Creates httpx.Client inside run() for thread safety.
        Emits response_received on success, error_occurred on failure.
        """
        try:
            with httpx.Client(timeout=30.0) as client:
                url = f"{self.api_url}chat/completions"
                payload = {
                    "model": self.model_name,
                    "messages": self.messages,
                    "stream": False
                }
                response = client.post(url, json=payload)
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

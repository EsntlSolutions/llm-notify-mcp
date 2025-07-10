"""LLM Notify MCP server implementation."""

import asyncio
import logging
import time

import pync
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field, field_validator

from .config import Config

logger = logging.getLogger(__name__)


class NotificationRequest(BaseModel):
    """Request model for notifications."""

    message: str = Field(..., max_length=140, description="Notification message")
    priority: str = Field("normal", description="Priority level")
    source: str | None = Field(None, description="Source identifier")

    @field_validator("message")
    @classmethod
    def validate_message(cls, v):
        if len(v.strip()) == 0:
            raise ValueError("Message cannot be empty")
        return v.strip()

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, v):
        if v not in ["low", "normal", "high"]:
            raise ValueError("Priority must be 'low', 'normal', or 'high'")
        return v


class NotificationResponse(BaseModel):
    """Response model for notifications."""

    success: bool
    message: str
    timestamp: float


class RateLimiter:
    """Simple rate limiter for notifications."""

    def __init__(self, max_requests: int, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: dict[str, list] = {}

    def is_allowed(self, client_id: str) -> bool:
        """Check if client is allowed to make a request."""
        now = time.time()

        if client_id not in self.requests:
            self.requests[client_id] = []

        # Remove old requests outside the window
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < self.window_seconds
        ]

        # Check if under limit
        if len(self.requests[client_id]) >= self.max_requests:
            return False

        # Add current request
        self.requests[client_id].append(now)
        return True


class NotificationServer:
    """Main notification server class."""

    def __init__(self, config: Config):
        self.config = config
        self.app = FastAPI(
            title="LLM Notify MCP",
            description="Local notification bridge for LLM agents",
            version="0.1.0"
        )
        self.rate_limiter = RateLimiter(config.rate_limit)
        self.security = HTTPBearer(auto_error=False) if config.auth_token else None
        self._setup_routes()

    def _verify_token(
        self, credentials: HTTPAuthorizationCredentials | None = None
    ) -> bool:
        """Verify authentication token if required."""
        if not self.config.auth_token:
            return True  # No auth required

        if not credentials:
            return False

        return credentials.credentials == self.config.auth_token

    def _setup_routes(self):
        """Set up FastAPI routes."""

        async def get_credentials(req: Request) -> HTTPAuthorizationCredentials | None:
            if self.security:
                return await self.security(req)
            return None

        @self.app.post("/notify", response_model=NotificationResponse)
        async def notify(
            request: NotificationRequest,
            req: Request,
            credentials: HTTPAuthorizationCredentials | None = Depends(get_credentials)
        ):
            """Send a notification."""

            # Check authentication
            if not self._verify_token(credentials):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication token"
                )

            # Get client IP for rate limiting
            client_ip = req.client.host

            # Check rate limit
            if not self.rate_limiter.is_allowed(client_ip):
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Rate limit exceeded"
                )

            # Send notification
            try:
                await self._send_notification(request)
                return NotificationResponse(
                    success=True,
                    message="Notification sent successfully",
                    timestamp=time.time()
                )
            except Exception as e:
                logger.error(f"Failed to send notification: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to send notification"
                )

        @self.app.get("/health")
        async def health():
            """Health check endpoint."""
            return {"status": "healthy", "timestamp": time.time()}

    async def _send_notification(self, request: NotificationRequest):
        """Send the actual notification."""

        # Send audio notification
        await self._send_audio_notification(request.message)

        # Send visual notification if enabled
        if self.config.visual_notifications:
            await self._send_visual_notification(request.message, request.priority)

    async def _send_audio_notification(self, message: str):
        """Send audio notification using macOS say command."""
        try:
            cmd = ["say"]
            
            # Only add voice parameter if specified (empty string uses system default)
            if self.config.voice:
                cmd.extend(["-v", self.config.voice])
            
            # Add speech rate and message
            cmd.extend(["-r", str(self.config.speech_rate), message])

            # Run say command asynchronously
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                logger.error(f"Say command failed: {stderr.decode()}")
                raise RuntimeError(f"Say command failed: {stderr.decode()}")

        except Exception as e:
            logger.error(f"Audio notification failed: {e}")
            raise

    async def _send_visual_notification(self, message: str, priority: str):
        """Send visual notification using pync."""
        try:
            title = "LLM Notify MCP"
            if priority == "high":
                title += " (High Priority)"

            # Run pync in thread to avoid blocking
            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: pync.notify(
                    message,
                    title=title,
                    appIcon=None,
                    contentImage=None,
                    sound="default" if priority == "high" else None
                )
            )

        except Exception as e:
            logger.error(f"Visual notification failed: {e}")
            # Don't raise - visual notifications are optional

    async def demo(self):
        """Send a demo notification."""
        demo_request = NotificationRequest(
            message="LLM Notify MCP is ready",
            priority="normal",
            source="demo"
        )
        await self._send_notification(demo_request)

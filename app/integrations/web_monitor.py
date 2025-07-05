from fastapi import FastAPI, Request, Response
from fastapi.middleware.base import BaseHTTPMiddleware
from ..threat_classifier import ThreatClassifier
from .alert_manager import AlertManager
import json
import re

class WebSecurityMonitor(BaseHTTPMiddleware):
    def __init__(
        self,
        app: FastAPI,
        alert_config: dict,
        excluded_paths: list = None
    ):
        super().__init__(app)
        self.classifier = ThreatClassifier(security_focus="web")
        self.alert_manager = AlertManager(alert_config)
        self.excluded_paths = excluded_paths or ["/health", "/metrics"]
        
        # Common attack pattern signatures
        self.attack_patterns = {
            "sql_injection": r"(?i)(union.*select|' *or *'1'='1|exec.*sp_|xp_cmdshell)",
            "xss": r"(?i)(<script>|javascript:|onload=|onerror=)",
            "path_traversal": r"(?i)(\.\.\/|\.\.\\|~\/)",
            "shell_injection": r"(?i)(&.*\||;.*\||`.*`)",
        }
    
    async def dispatch(
        self, request: Request, call_next
    ) -> Response:
        # Skip monitoring for excluded paths
        if request.url.path in self.excluded_paths:
            return await call_next(request)
            
        # Prepare log entry from request
        log_entry = await self._format_request_log(request)
        
        # Quick pattern check
        if self._check_attack_patterns(log_entry):
            # If patterns found, mark for immediate classification
            classification = await self.classifier.classify(log_entry)
            await self.alert_manager.process_classification(classification, log_entry)
            
            if classification.threat_level in ["HIGH", "CRITICAL"]:
                # Return 403 for high-risk requests
                return Response(
                    content="Access denied due to security risk",
                    status_code=403
                )
        
        # Continue with the request if no immediate threats
        response = await call_next(request)
        return response
    
    async def _format_request_log(self, request: Request) -> str:
        """Format request details for analysis"""
        # Get request body if available
        body = ""
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                raw_body = await request.body()
                body = raw_body.decode()
            except:
                body = "(unable to read body)"
        
        # Format the log entry
        return f"""
Web Request Details:
Method: {request.method}
Path: {request.url.path}
Query Params: {dict(request.query_params)}
Headers: {dict(request.headers)}
Client IP: {request.client.host}
Body: {body}
"""
    
    def _check_attack_patterns(self, log_entry: str) -> bool:
        """Quick check for known attack patterns"""
        for pattern in self.attack_patterns.values():
            if re.search(pattern, log_entry):
                return True
        return False
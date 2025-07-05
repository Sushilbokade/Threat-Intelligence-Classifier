import smtplib
import logging
from email.mime.text import MIMEText
from typing import Dict, Optional, List
import requests
from datetime import datetime

class AlertManager:
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Alert thresholds
        self.alert_thresholds = {
            "CRITICAL": 0.7,  # Alert on all critical with confidence > 70%
            "HIGH": 0.8,      # Alert on high threats with confidence > 80%
            "MEDIUM": 0.9     # Alert on medium threats only if very confident
        }
    
    async def process_classification(self, classification: Dict, log_entry: str):
        """Process a threat classification and send alerts if needed"""
        if self._should_alert(classification):
            await self._send_alerts(classification, log_entry)
    
    def _should_alert(self, classification: Dict) -> bool:
        """Determine if an alert should be sent based on threat level and confidence"""
        threshold = self.alert_thresholds.get(classification["threat_level"], 1.0)
        return classification["confidence"] >= threshold
    
    async def _send_alerts(self, classification: Dict, log_entry: str):
        """Send alerts through all configured channels"""
        message = self._format_alert_message(classification, log_entry)
        
        # Send to all configured channels
        if "slack" in self.config:
            await self.send_slack_alert(message, classification)
        
        if "email" in self.config:
            await self.send_email_alert(message, classification)
        
        if "webhook" in self.config:
            await self.send_webhook_alert(message, classification)
        
        # Always log the alert
        self.logger.warning(f"Security Alert: {message}")
    
    def _format_alert_message(self, classification: Dict, log_entry: str) -> str:
        """Format the alert message with all relevant details"""
        return f"""
Security Alert - {classification['threat_level']} Threat Detected
Time: {datetime.utcnow().isoformat()}
Confidence: {classification['confidence']:.2%}

Original Log:
{log_entry}

Analysis:
{classification['explanation']}

Recommended Action:
{self._get_recommended_action(classification['threat_level'])}
"""
    
    def _get_recommended_action(self, threat_level: str) -> str:
        """Get recommended actions based on threat level"""
        actions = {
            "CRITICAL": "Immediate action required. Investigate and contain the threat immediately.",
            "HIGH": "Investigate within 1 hour. Consider containment measures.",
            "MEDIUM": "Review within 24 hours. Monitor for escalation.",
            "LOW": "No immediate action required. Review during regular security assessment."
        }
        return actions.get(threat_level, "Review and classify manually")
    
    async def send_slack_alert(self, message: str, classification: Dict):
        """Send alert to Slack"""
        if "webhook_url" not in self.config["slack"]:
            self.logger.error("Slack webhook URL not configured")
            return
            
        emoji = {
            "CRITICAL": "🚨",
            "HIGH": "⚠️",
            "MEDIUM": "⚡",
            "LOW": "ℹ️"
        }
        
        try:
            response = requests.post(
                self.config["slack"]["webhook_url"],
                json={
                    "text": f"{emoji.get(classification['threat_level'], '❓')} {message}"
                }
            )
            response.raise_for_status()
        except Exception as e:
            self.logger.error(f"Failed to send Slack alert: {str(e)}")
    
    async def send_email_alert(self, message: str, classification: Dict):
        """Send alert via email"""
        if not all(k in self.config["email"] for k in ["smtp_server", "from_addr", "to_addrs"]):
            self.logger.error("Email configuration incomplete")
            return
            
        try:
            msg = MIMEText(message)
            msg['Subject'] = f"Security Alert: {classification['threat_level']} Threat Detected"
            msg['From'] = self.config["email"]["from_addr"]
            msg['To'] = ", ".join(self.config["email"]["to_addrs"])
            
            with smtplib.SMTP(self.config["email"]["smtp_server"]) as server:
                if "username" in self.config["email"]:
                    server.login(
                        self.config["email"]["username"],
                        self.config["email"]["password"]
                    )
                server.send_message(msg)
        except Exception as e:
            self.logger.error(f"Failed to send email alert: {str(e)}")
    
    async def send_webhook_alert(self, message: str, classification: Dict):
        """Send alert to a custom webhook"""
        if "url" not in self.config["webhook"]:
            self.logger.error("Webhook URL not configured")
            return
            
        try:
            response = requests.post(
                self.config["webhook"]["url"],
                json={
                    "message": message,
                    "classification": classification,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            response.raise_for_status()
        except Exception as e:
            self.logger.error(f"Failed to send webhook alert: {str(e)}")
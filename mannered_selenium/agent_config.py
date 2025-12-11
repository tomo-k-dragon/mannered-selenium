import os
import re

class AgentConfig:
    EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
    def __init__(self, name:str = None, version:str = None, email:str = None):
        # email format check.
        if email and not self.EMAIL_REGEX.fullmatch(email):
            raise ValueError(f"Invalid email format: {email}")

        elif not name and version:
            raise ValueError("When specify version, name is required.")
        elif not name:
            self.name = "*"
        else:
            self.name = name
        
        self.version = version
        self.email = email

    def build_user_agent(self) -> str:
        """
        build User-Agent header string.
        :return: agent_name/version(email) format string.
        """
        parts = []
        if self.name:
            version_part = f"/{self.version}" if self.version else ""
            parts.append(f"{self.name}{version_part}")
        if self.email:
            parts.append(f"({self.email})")
        
        return " ".join(parts)

    

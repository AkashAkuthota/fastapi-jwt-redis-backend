from dataclasses import dataclass
from database_models import User
from datetime import datetime

@dataclass
class AuthContext:
    user: User
    token: str
    expires_at: datetime

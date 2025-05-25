from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
import uuid

class Session:
    """
    Klasse om een sessie bij te houden met bijbehorende conversatiegeschiedenis en context.
    """
    def __init__(self, session_id: str = None, max_history: int = 20, ttl_hours: int = 24):
        """
        Initialiseer een nieuwe sessie.
        
        Args:
            session_id: Optionele unieke ID voor de sessie. Wordt automatisch gegenereerd indien niet opgegeven.
            max_history: Maximum aantal berichten dat wordt bijgehouden in de geschiedenis.
            ttl_hours: TTL (Time To Live) van de sessie in uren.
        """
        self.session_id = session_id or str(uuid.uuid4())
        self.created_at = datetime.now()
        self.last_accessed = self.created_at
        self.max_history = max_history
        self.ttl = timedelta(hours=ttl_hours)
        self.history: List[Dict[str, str]] = []
        self.context: Dict[str, Any] = {}
        
    def add_message(self, role: str, content: str) -> None:
        """Voeg een bericht toe aan de sessiegeschiedenis."""
        self.history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        # Beperk de geschiedenis tot max_history berichten
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
        self.last_accessed = datetime.now()
    
    def get_recent_history(self, max_messages: Optional[int] = None) -> List[Dict[str, str]]:
        """Haal de meest recente berichten op uit de geschiedenis."""
        if max_messages is None:
            return self.history
        return self.history[-max_messages:]
    
    def update_context(self, key: str, value: Any) -> None:
        """Werk de context van de sessie bij."""
        self.context[key] = value
        self.last_accessed = datetime.now()
    
    def get_context(self, key: str, default: Any = None) -> Any:
        """Haal een waarde op uit de context."""
        return self.context.get(key, default)
    
    def is_expired(self) -> bool:
        """Controleer of de sessie is verlopen."""
        return datetime.now() > (self.last_accessed + self.ttl)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converteer de sessie naar een dictionary voor serialisatie."""
        return {
            "session_id": self.session_id,
            "created_at": self.created_at.isoformat(),
            "last_accessed": self.last_accessed.isoformat(),
            "max_history": self.max_history,
            "ttl_hours": self.ttl.total_seconds() / 3600,
            "history": self.history,
            "context": self.context
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Session':
        """Maak een Session object van een dictionary."""
        session = cls(
            session_id=data["session_id"],
            max_history=data["max_history"],
            ttl_hours=data["ttl_hours"]
        )
        session.created_at = datetime.fromisoformat(data["created_at"])
        session.last_accessed = datetime.fromisoformat(data["last_accessed"])
        session.history = data["history"]
        session.context = data["context"]
        return session


class SessionManager:
    """
    Beheert meerdere sessies en zorgt voor opschoning van verlopen sessies.
    """
    def __init__(self):
        self.sessions: Dict[str, Session] = {}
    
    def create_session(self, **kwargs) -> Session:
        """Maak een nieuwe sessie aan en voeg deze toe aan de manager."""
        session = Session(**kwargs)
        self.sessions[session.session_id] = session
        return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Haal een sessie op bij ID. Retourneert None als de sessie niet bestaat of verlopen is."""
        session = self.sessions.get(session_id)
        if session is None:
            return None
        
        if session.is_expired():
            del self.sessions[session_id]
            return None
            
        return session
    
    def cleanup_expired(self) -> int:
        """Verwijder alle verlopen sessies en retourneer het aantal verwijderde sessies."""
        expired_ids = [
            session_id 
            for session_id, session in self.sessions.items()
            if session.is_expired()
        ]
        
        for session_id in expired_ids:
            del self.sessions[session_id]
            
        return len(expired_ids)
    
    def save_to_file(self, filepath: str) -> None:
        """Sla alle sessies op in een bestand."""
        data = {
            "sessions": {
                session_id: session.to_dict()
                for session_id, session in self.sessions.items()
            }
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'SessionManager':
        """Laad sessies uit een bestand."""
        manager = cls()
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for session_data in data.get("sessions", {}).values():
                session = Session.from_dict(session_data)
                if not session.is_expired():
                    manager.sessions[session.session_id] = session
                    
        except (FileNotFoundError, json.JSONDecodeError):
            # Bestand bestaat niet of is ongeldig, start met lege manager
            pass
            
        return manager

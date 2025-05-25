from typing import Dict, List, Optional, Any
from utils.ollama_client import OllamaClient
from utils.conversation_memory import Session, SessionManager

class BaseAgent:
    """
    Basisklasse voor alle agents met geïntegreerd sessiebeheer.
    """
    def __init__(
        self, 
        name: str,
        role: str,
        goal: str,
        backstory: str,
        llm: Optional[OllamaClient] = None,
        session_manager: Optional[SessionManager] = None,
        model: str = "openchat:latest"
    ):
        """
        Initialiseer de basis agent.
        
        Args:
            name: Naam van de agent
            role: Rol van de agent (bijv. 'Frontend Developer')
            goal: Doel van de agent
            backstory: Achtergrondinformatie over de agent
            llm: Optionele OllamaClient instantie
            session_manager: Optionele SessionManager instantie
            model: Naam van het te gebruiken LLM-model
        """
        self.name = name
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.llm = llm or OllamaClient(model=model)
        self.session_manager = session_manager or SessionManager()
    
    def get_or_create_session(self, session_id: str = None) -> Session:
        """
        Haal een bestaande sessie op of maak een nieuwe aan.
        
        Args:
            session_id: Optioneel sessie-ID. Wordt automatisch gegenereerd indien niet opgegeven.
            
        Returns:
            Een bestaande of nieuwe sessie
        """
        if session_id:
            session = self.session_manager.get_session(session_id)
            if session:
                return session
        
        # Maak een nieuwe sessie aan als deze niet bestaat
        return self.session_manager.create_session(session_id=session_id)
    
    def add_to_session(
        self, 
        session_id: str, 
        role: str, 
        content: str,
        update_context: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Voeg een bericht toe aan een sessie en werk eventueel de context bij.
        
        Args:
            session_id: ID van de sessie
            role: Rol van de afzender (bijv. 'user', 'assistant')
            content: Inhoud van het bericht
            update_context: Optionele context om bij te werken
        """
        session = self.get_or_create_session(session_id)
        session.add_message(role, content)
        
        if update_context:
            for key, value in update_context.items():
                session.update_context(key, value)
    
    def get_session_history(self, session_id: str, max_messages: Optional[int] = None) -> List[Dict[str, str]]:
        """
        Haal de gespreksgeschiedenis op voor een sessie.
        
        Args:
            session_id: ID van de sessie
            max_messages: Maximum aantal berichten om op te halen
            
        Returns:
            Lijst van berichten in de sessie
        """
        session = self.get_or_create_session(session_id)
        return session.get_recent_history(max_messages)
    
    def get_session_context(self, session_id: str, key: str, default: Any = None) -> Any:
        """
        Haal een waarde op uit de sessiecontext.
        
        Args:
            session_id: ID van de sessie
            key: Sleutel van de op te halen waarde
            default: Standaardwaarde als de sleutel niet bestaat
            
        Returns:
            De opgehaalde waarde of de standaardwaarde
        """
        session = self.get_or_create_session(session_id)
        return session.get_context(key, default)
    
    def update_session_context(self, session_id: str, key: str, value: Any) -> None:
        """
        Werk de sessiecontext bij.
        
        Args:
            session_id: ID van de sessie
            key: Sleutel van de bij te werken waarde
            value: Nieuwe waarde
        """
        session = self.get_or_create_session(session_id)
        session.update_context(key, value)
    
    def generate_response(
        self, 
        session_id: str, 
        user_input: str,
        system_prompt: Optional[str] = None,
        max_history: Optional[int] = 10
    ) -> str:
        """
        Genereer een antwoord op basis van de gebruikersinvoer en sessiegeschiedenis.
        
        Args:
            session_id: ID van de sessie
            user_input: Invoer van de gebruiker
            system_prompt: Optioneel aangepast systeemprompt
            max_history: Maximum aantal historische berichten om mee te sturen
            
        Returns:
            Het gegenereerde antwoord als string
        """
        # Voeg het gebruikersbericht toe aan de sessie
        self.add_to_session(session_id, "user", user_input)
        
        # Haal de gespreksgeschiedenis op
        conversation = self.get_session_history(session_id, max_messages=max_history)
        
        # Voeg een systeemprompt toe als die is opgegeven
        if system_prompt is None:
            system_prompt = (
                f"Jij bent {self.name}, een {self.role}. {self.backstory}\n"
                "Je antwoordt altijd in het Nederlands, tenzij anders gevraagd.\n"
                f"Je doel is: {self.goal}"
            )
        
        # Voeg het systeemprompt toe aan de conversatie
        full_conversation = [{"role": "system", "content": system_prompt}] + conversation
        
        # Genereer een antwoord met de LLM
        response = self.llm.generate_response(full_conversation)
        
        # Voeg het antwoord toe aan de sessie
        self.add_to_session(session_id, "assistant", response)
        
        return response
    
    def respond(
        self, 
        conversation: List[Dict[str, str]], 
        topic: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> str:
        """
        Abstracte methode die door subklassen moet worden geïmplementeerd.
        Genereer een antwoord op basis van het gespreksverloop.
        
        Args:
            conversation: Lijst van berichten in het formaat [{"role": "user", "content": "..."}, ...]
            topic: Optioneel onderwerp voor context
            session_id: Optioneel sessie-ID voor contextbehoud
            
        Returns:
            Het gegenereerde antwoord als string
        """
        raise NotImplementedError("Subklassen moeten deze methode implementeren")

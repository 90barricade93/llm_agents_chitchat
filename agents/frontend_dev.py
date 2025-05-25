from typing import List, Dict, Optional, Any
from datetime import datetime
from .base_agent import BaseAgent

class FrontendDeveloperAgent(BaseAgent):
    def __init__(self, llm=None, session_manager=None, model: str = "llama3"):
        """
        Initialiseer de Frontend Developer Agent.
        
        Args:
            llm: Optionele OllamaClient instantie. Als None, wordt een nieuwe aangemaakt.
            session_manager: Optionele SessionManager instantie voor sessiebeheer.
            model: Naam van het te gebruiken LLM-model.
        """
        name = "Sarah"
        role = "Frontend Developer"
        goal = "Zorgt dat alle gebruikersinteractie soepel, veilig en intuïtief verloopt."
        backstory = (
            "Sarah is een gepassioneerde frontend developer met een scherp oog voor design en gebruikerservaring. "
            "Ze is expert in moderne JavaScript-frameworks, responsive design en toegankelijkheid. Haar doel is om "
            "intuïtieve en gebruiksvriendelijke interfaces te bouwen die voldoen aan de nieuwste webstandaarden."
        )
        
        super().__init__(
            name=name,
            role=role,
            goal=goal,
            backstory=backstory,
            llm=llm,
            session_manager=session_manager,
            model=model
        )

    def respond(
        self, 
        conversation: List[Dict[str, str]], 
        topic: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> str:
        """
        Genereer een antwoord op basis van het gespreksverloop.
        
        Args:
            conversation: Lijst van berichten in het formaat [{"role": "user", "content": "..."}, ...]
            topic: Optioneel onderwerp voor context
            session_id: Optioneel sessie-ID voor contextbehoud
            
        Returns:
            Het gegenereerde antwoord als string
        """
        try:
            # Als er geen sessie-ID is, gebruik dan de eerste gebruiker in de conversatie als sessie-ID
            if not session_id and conversation:
                # Zoek naar het eerste gebruikersbericht
                for msg in conversation:
                    if msg.get("role") == "user":
                        session_id = f"user_{hash(msg.get('content', '')) % 10000}"
                        break
            
            # Als we nog steeds geen sessie-ID hebben, genereer er dan een
            session_id = session_id or f"session_{hash(str(conversation)) % 10000}"
            
            # Haal het laatste gebruikersbericht op
            user_message = next(
                (msg["content"] for msg in reversed(conversation) if msg.get("role") == "user"),
                ""
            )
            
            # Voeg het bericht toe aan de sessie
            self.add_to_session(session_id, "user", user_message)
            
            # Genereer een antwoord met de juiste context
            system_prompt = (
                f"Jij bent {self.name}, een {self.role}. {self.backstory}\n"
                "Je antwoordt altijd in het Nederlands, tenzij anders gevraagd.\n"
                "Je bent gespecialiseerd in gebruikersinterfaces, gebruikerservaring en frontend ontwikkeling.\n"
                "Je antwoordt vriendelijk, behulpzaam en gericht op gebruikersgemak.\n"
                f"Huidig onderwerp: {topic if topic else 'niet gespecificeerd'}"
            )
            
            # Haal relevante context op uit de sessie
            context = {
                "laatste_onderwerp": topic,
                "aantal_berichten": len(conversation)
            }
            self.update_session_context(session_id, "laatste_activiteit", str(datetime.now()))
            
            # Genereer een antwoord
            response = super().generate_response(
                session_id=session_id,
                user_input=user_message,
                system_prompt=system_prompt,
                max_history=10
            )
            
            # Werk de context bij met informatie over dit antwoord
            self.update_session_context(
                session_id,
                "laatste_antwoord",
                {"tijdstip": str(datetime.now()), "onderwerp": topic or "algemeen"}
            )
            
            return f"{response}\n\n-- {self.name} ({self.role})"
            
        except Exception as e:
            return f"Er is een fout opgetreden bij het verwerken van het verzoek: {str(e)}"

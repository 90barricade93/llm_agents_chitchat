import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta

# Voeg de root van het project toe aan het Python pad
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.base_agent import BaseAgent
from utils.conversation_memory import SessionManager, Session

class TestBaseAgent(unittest.TestCase):
    def setUp(self):
        """Maak een testagent aan voor elke test."""
        self.mock_llm = MagicMock()
        self.mock_llm.generate_response.return_value = "Test response"
        
        self.agent = BaseAgent(
            name="Test Agent",
            role="Test Role",
            goal="Test Goal",
            backstory="Test Backstory",
            llm=self.mock_llm
        )
    
    def test_initialization(self):
        """Test of de agent correct wordt geïnitialiseerd."""
        self.assertEqual(self.agent.name, "Test Agent")
        self.assertEqual(self.agent.role, "Test Role")
        self.assertEqual(self.agent.goal, "Test Goal")
        self.assertEqual(self.agent.backstory, "Test Backstory")
        self.assertIsNotNone(self.agent.session_manager)
    
    def test_get_or_create_session(self):
        """Test het ophalen of aanmaken van een sessie."""
        # Test het aanmaken van een nieuwe sessie
        session = self.agent.get_or_create_session("test_session")
        self.assertEqual(session.session_id, "test_session")
        
        # Test het ophalen van een bestaande sessie
        same_session = self.agent.get_or_create_session("test_session")
        self.assertIs(session, same_session)
    
    def test_add_to_session(self):
        """Test het toevoegen van een bericht aan een sessie."""
        self.agent.add_to_session("test_session", "user", "Hallo, hoe gaat het?")
        
        # Controleer of de sessie is aangemaakt en het bericht is toegevoegd
        session = self.agent.get_or_create_session("test_session")
        self.assertEqual(len(session.history), 1)
        self.assertEqual(session.history[0]["content"], "Hallo, hoe gaat het?")
        self.assertEqual(session.history[0]["role"], "user")
    
    def test_get_session_history(self):
        """Test het ophalen van de gespreksgeschiedenis."""
        # Voeg wat berichten toe aan de sessie
        self.agent.add_to_session("test_session", "user", "Eerste bericht")
        self.agent.add_to_session("test_session", "assistant", "Tweede bericht")
        
        # Haal de geschiedenis op
        history = self.agent.get_session_history("test_session")
        
        # Controleer of de geschiedenis correct is
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["content"], "Eerste bericht")
        self.assertEqual(history[1]["content"], "Tweede bericht")
    
    def test_session_context(self):
        """Test het bijwerken en ophalen van sessiecontext."""
        # Voeg wat context toe aan de sessie
        self.agent.update_session_context("test_session", "gebruiker_naam", "Jan")
        
        # Haal de context op en controleer of deze correct is
        naam = self.agent.get_session_context("test_session", "gebruiker_naam")
        self.assertEqual(naam, "Jan")
        
        # Test een niet-bestaande sleutel met standaardwaarde
        default = self.agent.get_session_context("test_session", "onbestaand", "standaard")
        self.assertEqual(default, "standaard")
    
    def test_generate_response(self):
        """Test het genereren van een antwoord met behoud van context."""
        # Stel de LLM mock in om een specifiek antwoord te retourneren
        self.agent.llm.generate_response.return_value = "Dit is een testantwoord."
        
        # Roep de methode aan
        response = self.agent.generate_response(
            session_id="test_session",
            user_input="Hallo, wie ben jij?",
            system_prompt="Jij bent een testassistent.",
            max_history=5
        )
        
        # Controleer of het antwoord correct is
        self.assertEqual(response, "Dit is een testantwoord.")
        
        # Controleer of de sessie is bijgewerkt
        session = self.agent.get_or_create_session("test_session")
        self.assertEqual(len(session.history), 2)  # Gebruikersbericht + antwoord
        self.assertEqual(session.history[0]["content"], "Hallo, wie ben jij?")
        self.assertEqual(session.history[1]["content"], "Dit is een testantwoord.")
        
        # Controleer of de LLM is aangeroepen met de juiste argumenten
        self.agent.llm.generate_response.assert_called_once()
        
        # Haal de argumenten op die aan generate_response zijn doorgegeven
        args, kwargs = self.agent.llm.generate_response.call_args
        
        # De conversatie zou het eerste argument moeten zijn
        full_conversation = args[0] if args else []
        
        # Controleer of de conversatie een lijst is
        self.assertIsInstance(full_conversation, list, "Conversation should be a list")
        
        # Controleer of we ten minste één bericht hebben
        self.assertGreater(len(full_conversation), 0, "Conversation should contain at least one message")
        
        # Controleer of de gebruikersinvoer in de conversatie zit
        user_input_found = any("Hallo, wie ben jij?" in str(msg.get("content", "")) for msg in full_conversation)
        self.assertTrue(user_input_found, "Gebruikersinvoer niet gevonden in de conversatie")
        
        # Controleer of het systeemprompt in de conversatie zit
        system_prompt_found = any("testassistent" in str(msg.get("content", "")).lower() for msg in full_conversation)
        self.assertTrue(system_prompt_found, "Systeemprompt niet gevonden in de conversatie")

if __name__ == "__main__":
    unittest.main()

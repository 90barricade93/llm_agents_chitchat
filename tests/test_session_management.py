import unittest
import os
import tempfile
import time
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

# Voeg de root van het project toe aan het Python pad
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.conversation_memory import Session, SessionManager

class TestSession(unittest.TestCase):
    def setUp(self):
        """Maak een nieuwe sessie aan voor elke test."""
        self.session = Session(session_id="test123", max_history=5, ttl_hours=1)
    
    def test_initialization(self):
        """Test of een nieuwe sessie correct wordt geïnitialiseerd."""
        self.assertEqual(self.session.session_id, "test123")
        self.assertEqual(self.session.max_history, 5)
        self.assertEqual(len(self.session.history), 0)
        self.assertEqual(len(self.session.context), 0)
    
    def test_add_message(self):
        """Test het toevoegen van berichten aan de sessie."""
        self.session.add_message("user", "Hallo, hoe gaat het?")
        self.assertEqual(len(self.session.history), 1)
        self.assertEqual(self.session.history[0]["role"], "user")
        self.assertEqual(self.session.history[0]["content"], "Hallo, hoe gaat het?")
    
    def test_history_limit(self):
        """Test of de geschiedenislimiet correct wordt toegepast."""
        for i in range(10):
            self.session.add_message("user", f"Bericht {i}")
        
        self.assertEqual(len(self.session.history), 5)  # max_history is 5
        self.assertEqual(self.session.history[0]["content"], "Bericht 5")  # Oudste bericht
        self.assertEqual(self.session.history[-1]["content"], "Bericht 9")  # Nieuwste bericht
    
    def test_context_management(self):
        """Test het toevoegen en ophalen van context."""
        self.session.update_context("gebruiker_naam", "Jan")
        self.session.update_context("voorkeuren", {"taal": "Nederlands", "thema": "donker"})
        
        self.assertEqual(self.session.get_context("gebruiker_naam"), "Jan")
        self.assertEqual(self.session.get_context("voorkeuren"), {"taal": "Nederlands", "thema": "donker"})
        self.assertIsNone(self.session.get_context("onbekende_sleutel"))
        self.assertEqual(self.session.get_context("onbekend", "standaard"), "standaard")
    
    def test_session_expiration(self):
        """Test of de sessie verloopt na de TTL."""
        # Maak een sessie aan die over 1 seconde verloopt
        session = Session(session_id="expire_test", ttl_hours=1/3600)  # 1 seconde TTL
        
        # Voeg een bericht toe om last_accessed bij te werken
        session.add_message("user", "Test")
        
        # Wacht even om zeker te zijn dat de sessie verloopt
        time.sleep(1.1)
        
        # Controleer of de sessie is verlopen
        self.assertTrue(session.is_expired())


class TestSessionManager(unittest.TestCase):
    def setUp(self):
        """Maak een nieuwe sessie manager aan voor elke test."""
        self.manager = SessionManager()
        self.session1 = self.manager.create_session(session_id="sessie1")
        self.session2 = self.manager.create_session(session_id="sessie2")
    
    def test_create_and_get_session(self):
        """Test het aanmaken en ophalen van sessies."""
        # Bestaande sessie ophalen
        session = self.manager.get_session("sessie1")
        self.assertEqual(session.session_id, "sessie1")
        
        # Onbekende sessie retourneert None
        self.assertIsNone(self.manager.get_session("onbekend"))
    
    def test_cleanup_expired(self):
        """Test het opruimen van verlopen sessies."""
        # Maak een sessie aan die direct verloopt
        expired_session = self.manager.create_session(
            session_id="expired", 
            ttl_hours=1/3600  # 1 seconde TTL
        )
        
        # Wacht even om zeker te zijn dat de sessie verloopt
        time.sleep(1.1)
        
        # Voeg nog een actieve sessie toe
        active_session = self.manager.create_session(session_id="active")
        
        # Voer cleanup uit
        removed = self.manager.cleanup_expired()
        
        # Controleer of alleen de verlopen sessie is verwijderd
        self.assertEqual(removed, 1)
        self.assertIsNone(self.manager.get_session("expired"))
        self.assertIsNotNone(self.manager.get_session("active"))
    
    def test_save_and_load_sessions(self):
        """Test het opslaan en laden van sessies naar een bestand."""
        # Maak een tijdelijk bestand
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            # Voeg wat berichten en context toe aan de sessies
            self.session1.add_message("user", "Hallo")
            self.session1.update_context("naam", "Testgebruiker")
            
            # Sla sessies op
            self.manager.save_to_file(temp_path)
            
            # Laad sessies opnieuw in
            new_manager = SessionManager.load_from_file(temp_path)
            
            # Controleer of de sessies correct zijn geladen
            loaded_session = new_manager.get_session("sessie1")
            self.assertIsNotNone(loaded_session)
            self.assertEqual(len(loaded_session.history), 1)
            self.assertEqual(loaded_session.history[0]["content"], "Hallo")
            self.assertEqual(loaded_session.get_context("naam"), "Testgebruiker")
            
        finally:
            # Opruimen
            if os.path.exists(temp_path):
                os.unlink(temp_path)


if __name__ == "__main__":
    unittest.main()

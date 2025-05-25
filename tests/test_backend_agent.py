import pytest
import json
from datetime import datetime
from unittest.mock import MagicMock, patch, ANY
from agents.backend_dev import BackendDeveloperAgent
from utils.conversation_memory import SessionManager

@pytest.fixture
def agent():
    # Maak een mock van de OllamaClient
    llm_mock = MagicMock()
    llm_mock.generate_response.return_value = "Dit is een testantwoord van de backend developer."
    
    # Maak een sessiebeheerder aan
    session_manager = SessionManager()
    
    # Geef een agent met de gemockte LLM en sessiebeheerder
    return BackendDeveloperAgent(llm=llm_mock, session_manager=session_manager)

def test_blijft_binnen_backend_domein(agent):
    # Arrange
    expected_response = "Dit is een frontend vraag, stel deze aan Sarah."
    agent.llm.generate_response.return_value = expected_response
    
    # Act
    conversation = [{"role": "user", "content": "Hoe valideer ik een formulier?"}]
    antwoord = agent.respond(conversation, topic="formuliervalidatie")
    
    # Assert
    agent.llm.generate_response.assert_called_once()
    assert expected_response in antwoord
    assert "Mark (Backend Developer)" in antwoord
    
    # Controleer of de sessie is bijgewerkt
    session = agent.get_or_create_session("user_" + str(hash("Hoe valideer ik een formulier?") % 10000))
    assert len(session.history) == 2  # Gebruikersvraag + antwoord

def test_api_response_handling(agent):
    # Arrange
    expected_response = "API response: Data succesvol opgehaald."
    agent.llm.generate_response.return_value = expected_response
    
    # Act
    conversation = [{"role": "user", "content": "Haal data op via de API."}]
    session_id = "test_api_session"
    antwoord = agent.respond(conversation, topic="API", session_id=session_id)
    
    # Assert
    agent.llm.generate_response.assert_called_once()
    assert expected_response in antwoord
    
    # Controleer of de sessie correct is bijgewerkt
    session = agent.get_or_create_session(session_id)
    assert len(session.history) == 2  # Vraag + antwoord
    assert session.history[0]["content"] == "Haal data op via de API."
    assert session.history[1]["content"] == expected_response
    
    # Controleer of de context is bijgewerkt
    assert "laatste_activiteit" in session.context
    assert "laatste_antwoord" in session.context
    assert session.context["laatste_antwoord"]["onderwerp"] == "API"

def test_api_status_feedback(agent):
    # Arrange
    expected_response = "API status: Operationeel. Alles werkt naar behoren."
    agent.llm.generate_response.return_value = expected_response
    
    # Act
    conversation = [{"role": "user", "content": "Wat is de status van de API?"}]
    session_id = "test_status_session"
    antwoord = agent.respond(conversation, topic="API status", session_id=session_id)
    
    # Assert
    agent.llm.generate_response.assert_called_once()
    assert expected_response in antwoord
    
    # Controleer of de sessie is bijgewerkt
    session = agent.get_or_create_session(session_id)
    assert len(session.history) == 2  # Vraag + antwoord
    assert "status" in session.history[0]["content"].lower()
    
    # Controleer of de context is bijgewerkt met het juiste onderwerp
    assert session.context["laatste_antwoord"]["onderwerp"] == "API status"
    assert expected_response in antwoord

def test_database_interactie(agent):
    # Arrange
    expected_response = "Record succesvol toegevoegd aan de database."
    agent.llm.generate_response.return_value = expected_response
    
    # Act
    conversation = [{"role": "user", "content": "Voeg een record toe aan de database."}]
    antwoord = agent.respond(conversation, topic="database")
    
    # Assert
    agent.llm.generate_response.assert_called_once()
    assert expected_response in antwoord

def test_email_functionaliteit(agent):
    # Arrange
    expected_response = "Bevestigingsmail is succesvol verzonden."
    agent.llm.generate_response.return_value = expected_response
    
    # Act
    conversation = [{"role": "user", "content": "Stuur een bevestigingsmail."}]
    antwoord = agent.respond(conversation, topic="e-mail")
    
    # Assert
    agent.llm.generate_response.assert_called_once()
    assert expected_response in antwoord

def test_doorverwijzing_naar_frontend(agent):
    # Arrange
    expected_response = "Dit is een frontend vraag. Sarah kan je hierbij helpen."
    agent.llm.generate_response.return_value = expected_response
    
    # Act
    conversation = [{"role": "user", "content": "Hoe verbeter ik de gebruikerservaring?"}]
    antwoord = agent.respond(conversation, topic="UX")
    
    # Assert
    agent.llm.generate_response.assert_called_once()
    assert expected_response in antwoord

def test_context_onthouden(agent):
    # Arrange
    session_id = "test_context_session"
    
    # Eerste bericht
    conversation1 = [{"role": "user", "content": "Mijn naam is Jan."}]
    agent.llm.generate_response.return_value = "Hallo Jan, hoe kan ik je helpen?"
    agent.respond(conversation1, session_id=session_id)
    
    # Tweede bericht - controleer of de naam wordt onthouden
    conversation2 = [
        {"role": "user", "content": "Mijn naam is Jan."},
        {"role": "assistant", "content": "Hallo Jan, hoe kan ik je helpen?"},
        {"role": "user", "content": "Weet je nog hoe ik heet?"}
    ]
    
    # Stel in dat de LLM een antwoord geeft met de naam uit de context
    def mock_generate_response(*args, **kwargs):
        # Controleer of de juiste context wordt doorgegeven
        if "Mijn naam is Jan" in str(kwargs.get("full_conversation", [])):
            return "Natuurlijk, je naam is Jan. Hoe kan ik je vandaag helpen?"
        return "Ik weet niet meer hoe je heet."
    
    agent.llm.generate_response.side_effect = mock_generate_response
    
    # Act
    antwoord = agent.respond(conversation2, session_id=session_id)
    
    # Assert
    assert "Jan" in antwoord
    
    # Controleer of de sessie alle berichten bevat
    session = agent.get_or_create_session(session_id)
    assert len(session.history) == 4  # 2 vragen + 2 antwoorden
    assert "Jan" in session.history[1]["content"]  # Eerste antwoord
    assert "Jan" in session.history[3]["content"]  # Tweede antwoord

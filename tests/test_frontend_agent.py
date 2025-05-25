import pytest
from unittest.mock import MagicMock, patch
from agents.frontend_dev import FrontendDeveloperAgent

@pytest.fixture
def agent():
    # Maak een mock van de OllamaClient
    llm_mock = MagicMock()
    llm_mock.generate_response.return_value = "Dit is een testantwoord van de frontend developer."
    
    # Geef een agent met de gemockte LLM
    return FrontendDeveloperAgent(llm=llm_mock)


def test_blijft_binnen_frontend_domein(agent):
    # Arrange
    expected_response = "Dit is een backend vraag. Mark kan je hierbij helpen."
    agent.llm.generate_response.return_value = expected_response
    
    # Act
    conversation = [{"role": "user", "content": "Kun je de database updaten?"}]
    antwoord = agent.respond(conversation, topic="database")
    
    # Assert
    agent.llm.generate_response.assert_called_once()
    assert expected_response in antwoord
    assert "Sarah (Frontend Developer)" in antwoord


def test_formuliervalidatie_feedback(agent):
    # Arrange
    expected_response = "Ja, test@example.com is een geldig e-mailadres."
    agent.llm.generate_response.return_value = expected_response
    
    # Act
    conversation = [{"role": "user", "content": "Is dit e-mailadres geldig: test@example.com?"}]
    antwoord = agent.respond(conversation, topic="formuliervalidatie")
    
    # Assert
    agent.llm.generate_response.assert_called_once()
    assert expected_response in antwoord


def test_gebruikersfeedback(agent):
    # Arrange
    expected_response = "Klik op de 'Verzenden' knop om het formulier in te dienen."
    agent.llm.generate_response.return_value = expected_response
    
    # Act
    conversation = [{"role": "user", "content": "Hoe kan ik het formulier indienen?"}]
    antwoord = agent.respond(conversation, topic="formulier")
    
    # Assert
    agent.llm.generate_response.assert_called_once()
    assert expected_response in antwoord


def test_doorverwijzing_naar_backend(agent):
    # Arrange
    expected_response = "Dit is een backend vraag. Mark kan je hierbij helpen met serverconfiguratie."
    agent.llm.generate_response.return_value = expected_response
    
    # Act
    conversation = [{"role": "user", "content": "Hoe configureer ik de server?"}]
    antwoord = agent.respond(conversation, topic="serverconfiguratie")
    
    # Assert
    agent.llm.generate_response.assert_called_once()
    assert expected_response in antwoord

@pytest.mark.skip(reason="Geheugen/context vereist sessie-implementatie")
def test_context_onthouden(agent):
    # TODO: Test dat Sarah context onthoudt tussen meerdere interacties
    pass

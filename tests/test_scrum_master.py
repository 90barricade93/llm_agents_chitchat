import pytest
from agents.scrum_master import ScrumMasterAgent
from unittest.mock import MagicMock

@pytest.fixture
def agent():
    llm_mock = MagicMock()
    llm_mock.generate_response.return_value = "Laten we het hebben over de voortgang."
    return ScrumMasterAgent(llm=llm_mock)


def test_begeleidt_gesprek(agent):
    # Arrange
    expected_response = "Laten we het teamoverleg starten. Wie wil er als eerste de voortgang delen?"
    agent.llm.generate_response.return_value = expected_response
    
    # Act
    conversation = [{"role": "user", "content": "Kun je het teamoverleg starten?"}]
    antwoord = agent.respond(conversation, topic="overleg")
    
    # Assert
    agent.llm.generate_response.assert_called_once()
    assert expected_response in antwoord
    assert "Erik (Scrum Master)" in antwoord


def test_bewaakt_rolgrenzen(agent):
    # Arrange
    expected_response = "Dat is een vraag voor Sarah, onze frontend developer. Sarah, kun je hier naar kijken?"
    agent.llm.generate_response.return_value = expected_response
    
    # Act
    conversation = [{"role": "user", "content": "Mark, kun jij de UI aanpassen?"}]
    antwoord = agent.respond(conversation, topic="rolbewaking")
    
    # Assert
    agent.llm.generate_response.assert_called_once()
    assert expected_response in antwoord


def test_doorverwijzing_tussen_developers(agent):
    # Arrange
    expected_response = "Laten we dit bespreken in het team. Sarah, Mark, kunnen jullie hier samen naar kijken?"
    agent.llm.generate_response.return_value = expected_response
    
    # Act
    conversation = [{"role": "user", "content": "Ik heb een backend en frontend issue."}]
    antwoord = agent.respond(conversation, topic="doorverwijzing")
    
    # Assert
    agent.llm.generate_response.assert_called_once()
    assert expected_response in antwoord


def test_neemt_geen_technische_beslissing(agent):
    # Arrange
    expected_response = "Dat is een technische beslissing. Laten we het team raadplegen. Wat denken jullie ervan?"
    agent.llm.generate_response.return_value = expected_response
    
    # Act
    conversation = [{"role": "user", "content": "Welke database moeten we gebruiken?"}]
    antwoord = agent.respond(conversation, topic="technische beslissing")
    
    # Assert
    agent.llm.generate_response.assert_called_once()
    assert expected_response in antwoord
    assert not any(w in antwoord.lower() for w in ["postgres", "mysql", "sqlite", "mongo"])


def test_vat_besluiten_samen(agent):
    # Arrange
    expected_response = "Laten ik de belangrijkste punten samenvatten: 1) We gaan door met het huidige plan, 2) Sarah en Mark werken samen aan de integratie, 3) Volgende check-in is morgen."
    agent.llm.generate_response.return_value = expected_response
    
    # Act
    conversation = [{"role": "user", "content": "Kun je de belangrijkste punten samenvatten?"}]
    antwoord = agent.respond(conversation, topic="samenvatting")
    
    # Assert
    agent.llm.generate_response.assert_called_once()
    assert expected_response in antwoord

@pytest.mark.skip(reason="Geheugen/context vereist sessie-implementatie")
def test_context_onthouden(agent):
    # TODO: Test dat Erik procescontext onthoudt tussen meerdere interacties
    pass

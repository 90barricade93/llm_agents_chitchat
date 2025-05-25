import pytest
from unittest.mock import MagicMock
from agents.frontend_dev import FrontendDeveloperAgent
from agents.backend_dev import BackendDeveloperAgent
from agents.scrum_master import ScrumMasterAgent

@pytest.fixture
def agents():
    # Maak aparte mocks voor elke agent
    llm_frontend = MagicMock()
    llm_frontend.generate_response.return_value = "Dat is een vraag voor Mark, onze backend developer."
    
    llm_backend = MagicMock()
    llm_backend.generate_response.return_value = "Sarah kan je hierbij helpen met frontend-vragen."
    
    llm_scrum = MagicMock()
    llm_scrum.generate_response.return_value = "Laten we de juiste persoon inschakelen voor deze vraag."
    
    return {
        "frontend": FrontendDeveloperAgent(llm=llm_frontend),
        "backend": BackendDeveloperAgent(llm=llm_backend),
        "scrum": ScrumMasterAgent(llm=llm_scrum),
    }

def test_interactie_roloverschrijding(agents):
    # Test frontend die backend-vraag krijgt
    conversation = [{"role": "user", "content": "Hoe update ik de database?"}]
    antwoord = agents["frontend"].respond(conversation, topic="database")
    
    # Controleer of de frontend doorverwijst naar de backend
    agents["frontend"].llm.generate_response.assert_called_once()
    assert "Mark" in antwoord or "backend" in antwoord.lower()
    
    # Reset de mock voor de volgende test
    agents["frontend"].llm.generate_response.reset_mock()
    
    # Test backend die frontend-vraag krijgt
    conversation = [{"role": "user", "content": "Hoe verbeter ik de gebruikerservaring?"}]
    antwoord = agents["backend"].respond(conversation, topic="UX")
    
    # Controleer of de backend doorverwijst naar de frontend
    agents["backend"].llm.generate_response.assert_called_once()
    assert "Sarah" in antwoord or "frontend" in antwoord.lower()


def test_scrum_master_rolbewaking(agents):
    # Test of de Scrum Master rolgrenzen bewaakt
    conversation = [{"role": "user", "content": "Sarah, kun jij de database aanpassen?"}]
    antwoord = agents["scrum"].respond(conversation, topic="rolbewaking")
    
    # Controleer of de Scrum Master correct reageert op roloverschrijding
    agents["scrum"].llm.generate_response.assert_called_once()
    # Controleer of het antwoord overeenkomt met de verwachte reactie van de Scrum Master
    expected_response = "Laten we de juiste persoon inschakelen voor deze vraag."
    assert expected_response in antwoord

@pytest.mark.skip(reason="Integratiegeheugen vereist sessie-implementatie")
def test_agents_delen_context(agents):
    """Test dat agents context kunnen delen in een sessie."""
    # Deze test wordt overgeslagen totdat sessiebeheer is geïmplementeerd
    pass

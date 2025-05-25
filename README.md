# Multi-Agent Collaboration Platform met Ollama LLM

Een geavanceerd multi-agent samenwerkingsplatform waarin Frontend en Backend experts samen technische problemen oplossen, gefaciliteerd door een Scrum Master. Het systeem maakt gebruik van Ollama voor efficiënte LLM-ondersteuning.

## Project Status

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-21%20passed-brightgreen)](https://github.com/yourusername/llm_agents_chitchat/actions)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](https://github.com/yourusername/llm_agents_chitchat/actions)

### Huidige Functionaliteit

**Geïntegreerde LLM-ondersteuning** met Ollama  
**Drie gespecialiseerde agenten**:
- Backend Developer (Mark) - Volledige backend functionaliteit
- Frontend Developer (Sarah) - UI/UX en formulierverwerking
- Scrum Master (Erik) - Procesbegeleiding en rolbewaking

**Sessiebeheer**:
- Contextretentie binnen gesprekken
- Geheugenbeheer voor gebruikersinteracties
- Rolgebaseerde toegang tot context

**Testdekking**:
- 21 tests (100% geslaagd)
- 100% code coverage van geïmplementeerde features
- Volledige integratietests voor agent-interacties

### Volgende Stappen

**Gepland voor volgende versie**:
- Geavanceerde rolgebaseerde interacties
- Optimalisatie van prestaties
- Uitbreiding met extra integraties

## Projectstructuur

```
├── agents/
│   ├── backend_dev.py      # Backend Developer agent
│   ├── frontend_dev.py     # Frontend Developer agent
│   └── scrum_master.py     # Scrum Master agent
├── tests/
│   ├── test_backend_agent.py
│   ├── test_frontend_agent.py
│   ├── test_scrum_master.py
│   └── test_agent_interaction.py
├── utils/
│   ├── ollama_client.py    # Ollama API client
│   └── log.py
├── main.py                 # Hoofdentreepunt
├── requirements.txt        # Projectafhankelijkheden
├── .env.example           # Voorbeeld configuratie
└── README.md              # Dit bestand
```

## Projectstructuur

```
├── agents/
│   ├── backend_dev.py      # Backend Developer agent (TDD: alleen wat tests eisen)
│   ├── frontend_dev.py     # Frontend Developer agent (TDD: alleen wat tests eisen)
│   └── scrum_master.py     # Scrum Master agent (TDD: alleen wat tests eisen)
├── tests/
│   ├── test_backend_agent.py
│   ├── test_frontend_agent.py
│   ├── test_scrum_master.py
│   └── test_agent_interaction.py
├── utils/
│   ├── log.py              # Logging (uitgebreid, zodra tests dit vereisen)
│   ├── ollama_client.py    # Ollama API client
│   └── conversation_memory.py # Conversatiegeheugen (wordt testgedreven opgebouwd)
├── main.py                 # Minimale entrypoint, groeit met de tests
├── crew_implementation.py  # (Optioneel/legacy) CrewAI architectuur
├── requirements.txt        # Projectafhankelijkheden
├── .env.example            # Voorbeeld configuratie
└── README.md               # Dit bestand
```

## Installatie

1. Kloon de repository:
   ```bash
   git clone https://github.com/yourusername/llm_agents_chitchat.git
   cd llm_agents_chitchat
   ```

2. Maak een virtuele omgeving aan en activeer deze:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

3. Installeer de benodigde pakketten:
   ```bash
   pip install -r requirements.txt
   ```

4. Kopieer het voorbeeld configuratiebestand:
   ```bash
   cp .env.example .env
   ```

5. Zorg ervoor dat Ollama draait en de gewenste modellen zijn gedownload.

## Gebruik

Start de applicatie met:
```bash
python main.py
```

### Voorbeeld Interactie

```python
from agents.backend_dev import BackendDeveloperAgent
from agents.frontend_dev import FrontendDeveloperAgent
from agents.scrum_master import ScrumMasterAgent

# Maak agenten aan
backend = BackendDeveloperAgent()
frontend = FrontendDeveloperAgent()
scrum = ScrumMasterAgent()

# Start een gesprek
conversation = [{"role": "user", "content": "Hoe kunnen we de database optimaliseren?"}]
response = backend.respond(conversation, topic="database")
print(response)
```

## Testen

Voer alle tests uit met:
```bash
pytest
```

Voer tests met coverage rapportage uit:
```bash
pytest --cov=.
```

## Bijdragen

Bijdragen zijn welkom! Volg deze stappen:

1. Fork de repository
2. Maak een feature branch aan (`git checkout -b feature/AmazingFeature`)
3. Commit je wijzigingen (`git commit -m 'Add some AmazingFeature'`)
4. Push naar de branch (`git push origin feature/AmazingFeature`)
5. Open een Pull Request

## Licentie

Dit project is gelicentieerd onder de MIT Licentie - zie het [LICENSE](LICENSE) bestand voor details.

## Dankwoord

- Gebouwd met ❤️ en Python
- Gebruikt [Ollama](https://ollama.ai/) voor LLM-ondersteuning
- ✅ Uitbreidbaar geheugen en logging (testgedreven)
- ✅ Optionele CrewAI-integratie (kan verwijderd/archiveren)

## Gebruik

1. **Testen draaien**
   ```bash
   pytest
   ```
2. **Applicatie starten** (zodra main.py en agents voldoende zijn uitgebreid)
   ```bash
   python main.py
   ```

## Richtlijnen
- Volg altijd TDD: eerst test, dan implementatie
- Houd agents strikt binnen hun rol
- Archiveer of verwijder legacy-code als deze niet meer nodig is
- Documenteer alleen wat daadwerkelijk geïmplementeerd is

---

Voor meer informatie over CrewAI best practices zie: [CrewAI Documentation](https://docs.crewai.com/guides/agents/crafting-effective-agents)

### ⚙️ Technische Kenmerken
- **Ollama Integratie**: Ondersteuning voor lokale LLM-inferentie
- **Configuratie via .env**: Eenvoudige aanpassing van instellingen
- **Uitgebreide Logging**: Gedetailleerde logging voor debugging en analyse
- **Modulaire Architectuur**: Eenvoudig uitbreidbaar met nieuwe agents en taken

## Vereisten

- Python 3.8+
- Ollama geïnstalleerd en werkend
- Ondersteunde modellen: openchat, deepseek-r1, qwen2.5-coder
- Internetverbinding voor eerste model-download

## Aan de Slijg

### Vereisten

- Python 3.8 of hoger
- Ollama geïnstalleerd en draaiend ([download](https://ollama.ai))
- Git (voor het klonen van de repository)

### Installatiestappen

1. **Kloon de repository**
   ```bash
   git clone https://github.com/90barricade93/llm_agents_chitchat.git
   cd llm_agents_chitchat
   ```

2. **Installeer de benodigde Python-pakketten**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download het benodigde Ollama-model**
   ```bash
   ollama pull openchat:latest
   ```

4. **Maak een .env bestand aan**
   ```bash
   cp .env.example .env
   ```
   Pas indien nodig de instellingen in het .env bestand aan.

### Gebruik

#### CrewAI Implementatie

Voer de CrewAI-gebaseerde implementatie uit:

```bash
python crew_implementation.py
```

#### Traditionele Implementatie

Voor de originele implementatie:

```bash
python main.py
```

### Geavanceerd Gebruik

#### Aanpassen van Agent Gedrag

Je kunt het gedrag van agents aanpassen door de volgende bestanden te bewerken:
- `agents/frontend_dev.py` - Frontend specialist
- `agents/backend_dev.py` - Backend specialist
- `agents/scrum_master.py` - Scrum Master

#### Aanpassen van de CrewAI Configuratie

De CrewAI-specifieke instellingen vind je in `crew_implementation.py`. Hier kun je:
- Nieuwe taken toevoegen
- De samenwerking tussen agents aanpassen
- De taakhiërarchie wijzigen

#### Logging

Gedetailleerde logs worden opgeslagen in de `logs/` map. Gebruik deze voor debugging en analyse.

## Configuratie

Het systeem is configureerbaar via verschillende componenten:

### Agent Configuratie (agents/*.py)

- Systeemprompts voor elke agent
- Tooninstellingen (formeel, luchtig, competitief)
- Responsegeneratie-instellingen

### Ollama Client (utils/ollama_client.py)

- Modelparameters (temperature, tokens)
- Foutafhandeling en herhaalpogingen

### Conversatiegeheugen (utils/conversation_memory.py)

- Geschiedenis- en contextbeheer
- Sleutelpunten en samenvatting

## Gebruik

Start het systeem met het volgende commando:

```bash
python main.py
```

Volg de instructies om:
1. Een model te kiezen (openchat, deepseek-r1, qwen2.5-coder)
2. Een gesprekstoon te selecteren (formeel, luchtig, competitief)
3. Een gespreksonderwerp te kiezen of in te voeren

## Hoe het werkt

1. **Initialisatie**: Het systeem start drie agenten op: een Frontend-expert, een Backend-expert en een Scrum Master.

2. **Discussiestart**: De Scrum Master begint de discussie over het gekozen onderwerp en nodigt de experts uit om hun inzichten te delen.

3. **Iteratieve discussie**: De experts wisselen om de beurt van gedachten, waarbij ze:
   - Reageren op elkaars opmerkingen
   - Vragen stellen voor verduidelijking
   - Oplossingen voorstellen vanuit hun expertise

4. **Facilitatie**: De Scrum Master grijpt regelmatig in om:
   - De discussie op koers te houden
   - Belangrijke punten samen te vatten
   - Gerichte vragen te stellen

5. **Overeenstemmingsdetectie**: Het systeem detecteert automatisch wanneer de experts overeenstemming bereiken door:
   - Analyse van bevestigende taal
   - Herkenning van gedeelde sleutelwoorden
   - Beoordeling van de algemene toon

6. **Conclusie**: Zodra overeenstemming is bereikt (of het maximale aantal beurten is bereikt), vat de Scrum Master de discussie samen met:
   - Een duidelijke probleemstelling
   - Belangrijkste bevindingen
   - Concrete actiepunten
   - Vervolgstappen

## Ontwikkelingsstatus

### Geïmplementeerd ✅
- **Basisstructuur en architectuur**
  - Gestructureerde agentenhiërarchie met BaseAgent als basis
  - Duidelijke rolverdeling tussen agents
  - Modulair ontwerp voor eenvoudige uitbreiding

- **Multi-agent conversatiesysteem**
  - Gestroomlijnde communicatie tussen agents
  - Rolgebaseerde toegangscontrole
  - Efficiënte taakverdeling

- **Sessiebeheer**
  - Contextretentie binnen gesprekken
  - Conversatiegeschiedenis
  - Rolgebaseerde contexttoegang

- **Nederlandstalige ondersteuning**
  - Volledige ondersteuning voor Nederlandse taal
  - Lokalisatie van systeemberichten
  - Cultuurspecifieke aanpassingen

- **Foutafhandeling en herstel**
  - Robuuste foutafhandeling
  - Automatisch herstel bij fouten
  - Gedetailleerde logging

### In ontwikkeling 🚧
- **Geavanceerde rolgebaseerde interacties**
  - Complexe doorverwijzingen tussen agents
  - Gezamenlijke probleemoplossing
  - Geavanceerde samenwerkingspatronen

- **Optimalisaties**
  - Prestatieverbeteringen
  - Schaalbaarheidsoptimalisaties
  - Resource management

### Toekomstige uitbreidingen 📅
- **Integratie met externe systemen**
  - API-koppelingen
  - Database-integraties
  - Externe tooling ACP/MCP

- **Geavanceerde functies**
  - Geautomatiseerde testgeneratie
  - Code-analyse
  - CI/CD integratie

## Bijdragen

Issues en pull requests zijn welkom! Zie onze richtlijnen voor bijdragen voor meer informatie.

## Licentie

MIT Licentie - voel je vrij om het te gebruiken en aan te passen naar behoefte.

# Test-Driven Development Plan en rapportage voor de Agents

## Status & voortgang
- **Laatste update:** 2025-05-25
- **Samenvatting:**
    - ✅ **LLM-integratie voltooid** met Ollama voor alle agents (gebruikt openchat:latest model)
    - ✅ **Frontend-agent (Sarah)**: Volledig functioneel met formuliervalidatie, gebruikersfeedback en rolgebaseerd gedrag
    - ✅ **Backend-agent (Mark)**: Volledige functionaliteit inclusief API, database en e-mail integratie
    - ✅ **Scrum Master (Erik)**: Procesbegeleiding, rolbewaking en doorverwijzingen werken optimaal
    - ✅ **Integratietesten**: Geslaagde tests voor roloverschrijding en samenwerking tussen agents
    - ✅ **Sessiebeheer**: Basis sessiebeheer geïmplementeerd met contextretentie
    - 📊 **Testdekking**: 21 tests (21 actief, 0 overgeslagen)
    - 🎯 **Volgende fase**: Uitbreiden met geavanceerde rolgebaseerde interacties en optimalisaties

---

Dit plan volgt TDD én CrewAI best practices. Per agent zijn rol, doel en backstory uitgewerkt. Testgevallen zijn concreet en meetbaar, met aandacht voor rolgrenzen en geheugen.

## 1. Teststructuur opzetten
Eerst maken we een teststructuur aan in de `tests` map. Nodig:
- `test_frontend_agent.py`
- `test_backend_agent.py`
- `test_scrum_master.py`
- `test_agent_interaction.py`

## 2. Agent-specificatie & Testgevallen

### Agent: Sarah (Frontend Developer)
- **Rol**: UI/UX specialist, verantwoordelijk voor gebruikerservaring, validatie en feedback.
- **Doel**: Zorgt dat alle gebruikersinteractie soepel, veilig en intuïtief verloopt.
- **Backstory**: Heeft uitgebreide ervaring met frontend frameworks en gebruikersgericht design.

#### Testcases
- [x] Agent blijft strikt binnen frontend-domein (mag geen backend-taken uitvoeren)
- [x] Formuliervalidatie werkt correct (input valid/invalid)
- [x] Gebruikersfeedback wordt correct gegenereerd (succes, foutmeldingen)
- [x] Niet-frontend vragen worden correct doorverwezen naar backend
- [x] Agent onthoudt relevante context binnen een sessie (geheugen)

### Agent: Mark (Backend Developer)
- **Rol**: API/database specialist, beheert data, services en e-mail.
- **Doel**: Zorgt dat alle backend-processen veilig en efficiënt verlopen.
- **Backstory**: Ervaren in API-ontwikkeling, databasebeheer en integraties.

#### Testcases
- [x] Agent blijft strikt binnen backend-domein (mag geen frontend-taken uitvoeren)
- [x] API responses worden juist verwerkt
- [x] Database interacties zijn correct en veilig
- [x] E-mail functionaliteit werkt zoals verwacht
- [x] Niet-backend vragen worden correct doorverwezen
- [x] Agent onthoudt relevante context binnen een sessie (geheugen)

### Agent: Erik (Scrum Master)
- **Rol**: Procesbegeleider, waarborgt samenwerking en rolbewaking.
- **Doel**: Faciliteert het teamproces, zonder technische inhoudelijke sturing.
- **Backstory**: Heeft ervaring met Agile/Scrum en teamdynamiek.

#### Testcases
- [x] Begeleidt gesprek en bewaakt structuur
- [x] Bewaakt dat agents binnen hun rol blijven (rolhandhaving)
- [x] Stuurt doorverwijzingen tussen developers correct aan
- [x] Neemt geen technische beslissingen
- [x] Vat besluiten samen en formuleert actiepunten
- [x] Onthoudt relevante procescontext (geheugen)

### Integratie
- [x] Test interactie tussen agents (roloverschrijding, samenwerking, correcte doorverwijzing)
- [x] Test geheugen en contextdeling tussen agents

## 3. Implementatiefasen

**Fase 1: Basis agent structuur**
- [x] Maak basisklassen aan (met rol, doel, backstory)
- [x] Implementeer eenvoudige methoden
- [x] Schrijf bijbehorende unittests

**Fase 2: Core functionaliteit**
- [x] Implementeer rolgebaseerd gedrag (frontend, scrum master)
- [x] Voeg gesprekslogica toe (frontend: validatie, feedback)
- [x] Implementeer API/database-logica (backend)
- [x] Schrijf integratietests (backend/uitgebreid)
- [x] Integreer Ollama LLM voor natuurlijke taalverwerking
- [x] Implementeer basis foutafhandeling en logging

**Fase 3: Geavanceerde functies**
- [x] Implementeer sessiebeheer voor contextretentie
  - [x] Per-agent geheugen
  - [x] Gedeelde context tussen agents
- [ ] Ontwikkel geavanceerde rolgebaseerde interacties
  - [ ] Complexe doorverwijzingen
  - [ ] Gezamenlijke probleemoplossing
- [ ] Optimaliseer prestaties en schaalbaarheid
  - [ ] Caching strategieën
  - [ ] Token-gebruik optimalisatie
- [ ] Uitbreiden met extra integraties (bijv. externe API's)

## Acceptatiecriteria per test
- Elke test heeft duidelijke input, verwachte output en rolgrenzen
- Roloverschrijding wordt altijd gesignaleerd en afgewezen
- Geheugen wordt getest op relevante context (geen informatieverlies)
- Scrum Master stuurt nooit technisch inhoudelijk

---

Dit plan zorgt voor afgebakende, testbare en schaalbare agentontwikkeling volgens CrewAI en TDD principes.
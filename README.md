# Idé- och Behovshubben - Projektdokumentation

## Projektöversikt
System för att samla in, analysera och utveckla medarbetarnas idéer, behov och utmaningar till framtidens tjänster. Bygger på innovationsguiden.se metodiken för användardriven innovation i offentlig sektor.

## Nuvarande Status
✅ **Klickbar prototyp färdig** - `index.html`
- Komplett UI/UX design
- 5 huvudsektioner implementerade
- Responsiv design
- Mockup-data för demonstration

## Systemarkitektur (Planerad)

### Kärnfunktioner
1. **Insamlingsmodul**
   - Multi-kanal insamling (web, mobil, API)
   - Strukturerade formulär baserat på innovationsguiden
   - Kategorisering: Idéer, behov, utmaningar, förbättringsförslag

2. **Analys- och Mappningsmodul**
   - AI-driven kategorisering och analys
   - Automatisk mappning mot befintlig tjänsteportfölj
   - Gap-analys och prioritering
   - Sentiment- och trendanalys

3. **Visualisering och Transparens**
   - Real-time dashboard med KPI:er
   - Interaktiva grafer och trender
   - Anonymiserad feedbackloop

4. **Roadmap och Styrning**
   - Automatisk roadmap-generering
   - Integration med besluts- och styrprocesser
   - Kapacitets- och resursplanering

## Designbeslut och Lärdomar

### Integration med Innovationsguiden
- **Metodik**: 6-stegs process för användardriven innovation
- **Fokus**: "Göra rätt saker" snarare än nya saker
- **Approach**: Iterativt och kollaborativt
- **Målgrupp**: Medarbetare som behöver stöd i den tidiga processen

### UX/UI Principer
- **Mobile-first**: Många idéer uppstår spontant
- **Transparens**: Alla kan följa status på inlämnade bidrag
- **Gamification**: Uppmuntra delaktighet genom engagemang
- **Enkelhet**: Låg tröskel för att lämna idéer

### Datamodell (Konceptuell)
```
Idé/Behov:
- Typ (idé, problem, behov, förbättring)
- Titel och beskrivning
- Målgrupp (medborgare, företag, medarbetare, andra org)
- Prioritet (låg, medel, hög)
- Status (ny, granskning, utveckling, implementerad)
- Mappning mot befintliga tjänster
- AI-genererade tags och kategorier
```

## Nästa Steg (Prioriterat)

### Fas 1 - MVP Foundation (2-3 månader)
1. **Backend-arkitektur**
   - Databas design och implementation
   - REST API för CRUD-operationer
   - Användarhantering och behörigheter

2. **AI-integration**
   - Text-analys för automatisk kategorisering
   - Sentiment-analys
   - Mappning mot befintlig tjänstekatalog

3. **Integration befintliga system**
   - SSO-integration
   - API-kopplingar till befintliga processer
   - Export-funktioner för data

### Fas 2 - Enhanced Analytics (3-4 månader)
1. **Avancerad analys**
   - Prediktiv modellering
   - Trendanalys över tid
   - ROI-beräkningar för implementerade idéer

2. **Kollaboration**
   - Kommentarsfunktion
   - Expertkoppling
   - Idé-utveckling i grupp

### Fas 3 - Process Integration (2-3 månader)
1. **Styrning och beslutsfattande**
   - Automatiserade arbetsflöden
   - Integration med projektportfölj
   - Budgetplanering och resurstilldelning

## Tekniska Överväganden

### Föreslagna Teknologier
- **Frontend**: React/Vue.js för interaktivitet
- **Backend**: Node.js/Python för API och AI-integration
- **Databas**: PostgreSQL för strukturerad data
- **AI/ML**: OpenAI API eller liknande för textanalys
- **Hosting**: Cloud-native (Azure/AWS) för skalbarhet

### Säkerhet och Compliance
- GDPR-compliance för personuppgifter
- Anonymiseringstekniker för transparens
- Säker hantering av känsliga organisationsdata
- Audit-loggar för spårbarhet

### Integrationspunkter
- **Befintliga system**: HR, ärendehantering, projektportfölj
- **Externa API:er**: Innovationsguiden.se resurser
- **Rapporteringsverktyg**: BI-system för ledningsrapportering

## Identifierade Risker och Utmaningar

1. **Användaradoption**: Risk att medarbetare inte använder systemet
   - *Mitigation*: Fokus på enkelhet och tydlig värdeproposition

2. **Informationsöverbelastning**: För många idéer att hantera
   - *Mitigation*: AI-driven prioritering och filtrering

3. **Integration komplexitet**: Många befintliga system att koppla mot
   - *Mitigation*: Fasa integration och börja med enklaste kopplingarna

4. **Förväntningshantering**: Medarbetare förväntar sig snabb implementation
   - *Mitigation*: Tydlig kommunikation om process och tidsramar

## Status & Aktuell Implementation

### 🎯 Aktuell Status (2025-11-10)
✅ **Komplett modulärt system implementerat och Docker-deployat**:
- **FastAPI backend** med SQLite databas
- **AI-analys** med Qwen3 32B via OpenRouter
- **Service mapping** mot tjänstekatalog (202 tjänster som separata dokument)
- **Responsiv frontend** med 5 huvudsektioner (inkl. Dokument-hantering)
- **Real-time visualiseringar** för analysinformation
- **Docker deployment** - Fullt fungerande med docker-compose (8.27GB image)
- **Röstnings- och kommentarssystem** - Användare kan rösta och kommentera idéer
- **Automatisk tjänstekatalog-import** - Varje tjänst laddas som separat dokument för optimal RAG-matchning

### ✨ Implementerade Features

#### Backend (innovation_hub/)
- **Database Models** (`database/models.py`):
  - Users, Categories, Ideas, Tags, Comments
  - AI analysis results (sentiment, confidence, notes)
  - Service mapping data (recommendation, confidence, matching services)

- **API Endpoints** (`api/main.py`, `api/documents.py`):
  - `/api/ideas` - CRUD för idéer med AI-analys
  - `/api/ideas/{id}/analyze` - Omanalys med service mapping
  - `/api/ideas/{id}/vote` - Toggle röst på idé (NY 2025-10-08)
  - `/api/ideas/{id}/comments` - CRUD för kommentarer (NY 2025-10-08)
  - `/api/analysis/stats` - Komplett analysstatistik
  - `/api/documents/upload` - Ladda upp dokument med **automatisk tjänstekatalog-detektion** (UPPDATERAD 2025-11-10)
  - `/api/documents/upload-service-catalog` - Specialiserad endpoint för tjänstekataloger
  - `/api/documents/files` - Lista unika filer i RAG
  - `/api/documents/{filename}` - Ta bort specifik fil
  - `/api/documents/clear` - Rensa hela RAG-databasen
  - `/api/categories`, `/api/tags`
  - Auto-dokumentation: `/docs`

- **AI Services** (`ai/`):
  - `openrouter_client.py` - Qwen3 32B integration
  - `analysis_service.py` - Komprehensiv AI-analys (kategori, prioritet, tags, sentiment, status)
  - `service_mapper.py` - Mappar idéer mot befintlig tjänstekatalog
  - `embeddings_client.py` - Genererar semantiska embeddings för RAG
  - `rag_service.py` - ChromaDB RAG-system för dokumentlagring och sökning
  - `rag_service_mapper.py` - RAG-baserad semantisk tjänstematchning (top_k=10, uppdaterad 2025-10-08)
  - `document_processor.py` - Dokumentbehandling och chunking
  - `service_catalog_loader.py` - Laddar tjänstekatalog som separata RAG-dokument

- **CRUD Operations** (`api/crud.py`, `api/analysis_crud.py`):
  - Idéhantering med AI-förbättring
  - Analysstatistik och aggregering
  - Service matching och gap-analys

- **Utility Scripts**:
  - `start.py` - Smart startup med databaspersistens
  - `reset_database.py` - Manuell databasreset (NY 2025-10-08)
  - `clean_rag.py` - Rensa temporära filer från RAG (NY 2025-10-08)

#### Frontend (innovation_hub/frontend/)
**4 Huvudsektioner:**

1. **🕐 Senaste Idéer**
   - Visar de 20 senast inlämnade idéerna
   - Kompakt översikt med alla detaljer

2. **➕ Lämna Idé**
   - Formulär för nya idéer/behov/problem
   - AI-analys körs automatiskt vid inlämning
   - Auto-kategorisering och taggning

3. **📋 Bläddra Idéer**
   - Filtrera på status, typ, prioritet, målgrupp
   - Sök i titel och beskrivning
   - Detaljerad listvy med fullständig information
   - **✏️ Redigera idéer** - Ändra titel, beskrivning, typ och målgrupp (2025-10-08)
   - **🔄 Omanalysera** - Kör AI-analys och service mapping på nytt efter ändringar (2025-10-08)

4. **🧠 Analys**
   - **Service Mapping Overview**: 4 färgkodade kort (befintlig/utveckla/ny/totalt)
   - **Utvecklingsbehov Matrix**: 3x3 grid (prioritet × service-typ)
   - **Top Matchade Tjänster**: Lista med de mest matchade tjänsterna
   - **Gap-analys**: Identifierar områden utan befintliga tjänster
   - **AI Confidence Meter**: Visar analysens tillförlitlighet

5. **📄 Dokument** (2025-10-08)
   - **RAG-databas hantering** - Se alla dokument i ChromaDB
   - **Ta bort individuella filer** - Rensa specifika dokument från RAG
   - **Rensa alla** - Ta bort hela RAG-databasen med dubbelbekräftelse
   - **Statistik** - Visa antal chunks, dokument, och filtyper
   - **Drag & drop uppladdning** - Ladda upp nya dokument till RAG

### 🔄 Service Mapping Process

När en idé lämnas in:
1. **AI-analys** kategoriserar och prioriterar (Qwen3 32B)
2. **Keyword extraction** från titel och beskrivning
3. **Tjänstekatalog-sökning** bland 202 befintliga tjänster
4. **Matchningsalgoritm** beräknar likhetspoäng
5. **Rekommendation** ges:
   - **Befintlig tjänst** (≥60% match) - Kan mötas med befintlig lösning
   - **Utveckla befintlig** (30-60% match) - Befintlig tjänst kan utökas
   - **Ny tjänst** (<30% match) - Kräver ny utveckling

### 🧠 RAG System (Retrieval-Augmented Generation)

**Implementerat RAG-system för semantisk tjänstematchning:**

**ChromaDB Vector Database:**
- **268 totala dokument** i RAG-samlingen
- **202 tjänster** från tjänstekatalogen som separata dokument
- **66 chunks** från XLS-tjänstekatalog för fallback
- Persisterad i `./chroma_db/` directory

**Dokumentstruktur per tjänst:**
```
Tjänst: [Tjänstenamn]
Beskrivning: [Beskrivning av tjänsten]
Startdatum: [När tjänsten började]
Detta är en befintlig tjänst som kan användas eller utvecklas för att möta liknande behov.
```

**Metadata per tjänst:**
- `service_name` - Unikt tjänstenamn som identifier
- `service_type: 'municipal_service'` - Typ av tjänst
- `start_date` - När tjänsten började
- `source: 'service_catalog'` - Källa för dokumentet

**Embeddings:**
- Genereras med `EmbeddingsClient`
- Semantisk sökning möjliggör intelligent matchning
- Varje tjänst lagras som 1 komplett dokument (ej chunkad) för optimal RAG-matchning

**Användning:**
- `RAGServiceMapper` använder RAG för semantisk matchning mellan idéer och tjänster
- Fallback till keyword-baserad matching vid låg tillförlitlighet
- Möjliggör framtida NLP-baserad analys och rekommendationer

### 💻 Starta systemet:

**Lokalt (Development):**
```bash
cd /home/frehal0707/use_cases
source venv/bin/activate
python start.py
# → http://localhost:8000
# → API Docs: http://localhost:8000/docs
```

**Docker (Local Testing):**
```bash
# Quick test
./test-docker.sh

# Or with docker-compose
docker compose up -d
# → http://localhost:8000
```

**OpenShift (Production):**
```bash
# Deploy to OpenShift
oc apply -k k8s/
# → https://innovation-hub.apps.your-cluster.com
```

See [QUICKSTART.md](QUICKSTART.md) for OpenShift deployment or [LOCAL_TESTING.md](LOCAL_TESTING.md) for Docker testing.

### 📁 Projektstruktur

```
/home/frehal0707/use_cases/
├── innovation_hub/              # Huvudapplikation
│   ├── __init__.py
│   ├── database/                # Databasmodeller
│   │   ├── models.py           # SQLAlchemy modeller
│   │   └── connection.py       # DB connection
│   ├── models/                  # Pydantic schemas
│   │   └── schemas.py          # API request/response modeller
│   ├── api/                     # FastAPI endpoints
│   │   ├── main.py             # API routes
│   │   ├── crud.py             # CRUD operationer
│   │   └── analysis_crud.py    # Analysstatistik
│   ├── ai/                      # AI-tjänster
│   │   ├── openrouter_client.py # OpenRouter API-klient
│   │   ├── analysis_service.py  # AI-analys service
│   │   ├── service_mapper.py    # Keyword-baserad tjänstemappning
│   │   ├── embeddings_client.py # Embedding-generering för RAG
│   │   ├── rag_service.py       # ChromaDB RAG-tjänst
│   │   ├── rag_service_mapper.py # RAG-baserad semantisk matchning
│   │   ├── document_processor.py # Dokumentbehandling
│   │   └── service_catalog_loader.py # Laddar tjänstekatalog till RAG
│   ├── frontend/                # Web-gränssnitt
│   │   ├── index.html          # Huvudsida
│   │   ├── css/main.css        # Styling
│   │   └── js/
│   │       ├── api.js          # API-klient
│   │       ├── ui.js           # UI-komponenter
│   │       ├── analysis.js     # Analysvisualisering
│   │       ├── documents.js    # RAG-dokumenthantering
│   │       ├── edit.js         # Idéredigerare med omanalys
│   │       └── main.js         # Huvudlogik
│   └── tests/                   # Test utilities
│       └── seed_data.py        # Testdata
├── existingservicesandprojects/ # Tjänstekatalog
│   └── tjanstekatalog-export-2025-10-07_12_40_39.xls
├── chroma_db/                   # ChromaDB RAG vector database
│   ├── chroma.sqlite3          # Vector store
│   └── [collection data]        # 202 services + 66 chunks
├── .env                         # Konfiguration
├── requirements.txt             # Python dependencies
├── start.py                     # Startup script
└── innovation_hub.db           # SQLite databas
```

### 🔑 Konfiguration (.env)

```bash
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
AI_MODEL=qwen/qwen3-32b
DATABASE_URL=sqlite:///./innovation_hub.db
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

### 📊 Tjänstekatalog

- **202 tjänster** från befintlig katalog
- **Kategorier**: IT och Digital (120), Övrig (41), Säkerhet (16), Kommunikation (16), Transport (6)
- **Automatisk kategorisering** baserad på nyckelord
- **Keyword index** för snabb sökning

### 🚀 Nästa Utvecklingssteg

**✅ Implementerat (2025-10-08):**
1. ✅ **Redigera idéer** - Fullständig edit-modal med omanalys
2. ✅ **RAG-hantering i GUI** - Ta bort individuella filer eller hela databasen
3. ✅ **Service mapping vid omanalys** - Automatisk uppdatering av tjänsterekommendationer
4. ✅ **Databaspersistens** - Data bevaras vid server-omstart
5. ✅ **Förbättrad service matching** - Ökad täckning (top_k från 5 till 10)
6. ✅ **Dokumentation** - Komplett changelog och feature-dokumentation

**🔄 Pågående Problem:**
- CSS-bugg: "Ta bort"-knappar i Dokument-fliken endast synliga vid hover (pågående troubleshooting)

**Fas 2 - Enhanced Features:**
1. Användarautentisering (SSO)
2. Kommentarsfunktion på idéer
3. Export till Excel/PDF
4. Email-notifikationer
5. Tidsserieanalys av trender
6. Interaktiva grafer (Chart.js/D3.js)
7. **RAG-baserad semantisk sökning i UI** - Använd embeddings för bättre sökresultat
8. **Versionshistorik för idéer** - Se tidigare versioner och återställ
9. **Förbättra Smart stad-beskrivning** - Lägg till IoT-exempel för bättre matchning

**Fas 3 - Advanced Analytics:**
1. Prediktiv analys av framtida behov
2. ROI-beräkningar för implementerade idéer
3. Automatiska rekommendationer för prioritering
4. Integration med projektportföljsystem
5. **Hybrid RAG + Keyword matching** - Kombinera båda metoderna för optimal precision
6. **Batch-analys** - Analysera flera idéer samtidigt
7. **Cachning av AI-resultat** - Snabbare omanalys

## Ytterligare Idéer att Utforska

1. **Gamification**: Poängsystem, badges, leaderboards
2. **AI-assistenter**: Chatbot som hjälper till att formulera idéer
3. **Prediktiv analys**: Förutsäga framtida behov baserat på trender
4. **Expertmatchning**: Koppla idéer till rätt kompetenser automatiskt
5. **Impact tracking**: Mäta faktisk effekt av implementerade idéer
6. **Cross-organisational sharing**: Dela lärdomar med andra organisationer

---

## 📋 Changelog

**2025-11-10:**
- 🐳 Docker deployment fully working (8.27GB image, docker-compose ready)
- 🔧 Fixed SQLAlchemy 2.0 compatibility issues
- 🔧 Fixed volume permission issues for Docker
- 📦 Automatic service catalog detection in upload endpoint
- ✅ Tested full system: AI analysis, voting, service mapping
- 📚 202 services loaded as separate documents in RAG (verified working)
- 🎯 Service matching tested and verified (IoT → CIP Platform match)

**2025-10-28:**
- 🚀 Complete OpenShift deployment package (27 files)
- 📝 7 comprehensive deployment guides (~10,000 words)
- 🔐 Production-ready security and resilience features
- 🔄 GitLab CI/CD pipeline + ArgoCD GitOps

**2025-10-08:**
- ✏️ Edit ideas functionality with re-analysis option
- 🗑️ RAG database management in GUI (delete files individually or all)
- 💾 Database persistence across server restarts
- 🔍 Improved service mapping coverage (top_k: 5 → 10)
- 👍 Voting system implemented
- 💬 Comment system added
- 📝 Comprehensive documentation (CHANGELOG, EDIT_IDEA_FEATURE, RAG_MANAGEMENT)

**2025-10-07:**
- 🧠 RAG System implementation with ChromaDB
- 📊 202 services loaded as individual documents
- 🎯 Semantic service matching with embeddings
- 📈 Analysis dashboard with service mapping visualization

**2024-10-03:**
- 🎨 Initial prototype and design
- 📄 Project documentation
- 💡 Concept and architecture planning

---
*Skapad: 2024-10-03*
*Senast uppdaterad: 2025-11-10 - Docker Deployment & Service Catalog Auto-Detection*
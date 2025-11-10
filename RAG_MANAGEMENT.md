# RAG-hantering - Dokumentation

## Översikt
Innovation Hub har nu fullt stöd för att hantera dokument i RAG-vektordatabasen (ChromaDB).

## Funktioner

### 1. Via Kommandorad (Script)
Använd `clean_rag.py` för att ta bort temporära filer:

```bash
cd /home/frehal0707/use_cases
source venv/bin/activate
python clean_rag.py
```

**Vad scriptet gör:**
- Visar statistik över RAG-databasen
- Hittar alla filer som innehåller "tmp" i namnet
- Tar bort dessa filer och alla deras chunks
- Visar uppdaterad statistik

### 2. Via Web-gränssnitt
Öppna **Dokument**-fliken i Innovation Hub: http://localhost:8000

#### Funktioner i GUI:

**📊 RAG-statistik**
- Totalt antal chunks
- Antal unika dokument
- Fördelning av filtyper

**📄 Uppladdade Dokument**
- Lista över alla dokument med:
  - Filnamn
  - Källa (🏛️ Tjänstekatalog eller 📄 Dokument)
  - Antal chunks
  - Filtyp
  - Uppladdningsdatum
  - **Ta bort**-knapp per fil
  - **Rensa alla**-knapp (med dubbel bekräftelse)

**⬆️ Ladda upp Dokument**
- Dra och släpp filer
- Stödjer: PDF, Word, Excel, Text
- Automatisk embeddings-generering
- Läggs till i RAG-systemet

### 3. Via API

#### Lista alla filer
```bash
GET /api/documents/files
```

Returnerar:
```json
[
  {
    "filename": "APN (mobil uppkoppling)",
    "chunk_count": 1,
    "file_type": "text",
    "source": "service_catalog",
    "service_type": "municipal_service",
    "first_seen": "2025-10-07T16:14:12.070129"
  }
]
```

#### Ta bort en fil
```bash
DELETE /api/documents/{filename}
```

Exempel:
```bash
curl -X DELETE "http://localhost:8000/api/documents/tmp7om2ussc.xls"
```

Returnerar:
```json
{
  "filename": "tmp7om2ussc.xls",
  "chunks_deleted": 66,
  "status": "success"
}
```

#### Rensa hela databasen
```bash
POST /api/documents/clear
```

**⚠️ VARNING:** Tar bort ALLA dokument permanent!

```bash
curl -X POST "http://localhost:8000/api/documents/clear"
```

#### Statistik
```bash
GET /api/documents/stats
```

Returnerar:
```json
{
  "total_chunks": 202,
  "unique_documents": 202,
  "file_types": {
    "text": 202
  },
  "collection_name": "service_documents"
}
```

## Säkerhet

### Dubbelbekräftelse för "Rensa alla"
I GUI:n får användaren två varningar innan alla dokument raderas:
1. ⚠️ Första varningen: "Är du säker?"
2. 🚨 Andra varningen: "SISTA VARNINGEN"

Detta förhindrar oavsiktlig borttagning.

## Användningsfall

### Ta bort gammal tjänstekatalog och ladda upp ny
1. Gå till **Dokument**-fliken
2. Klicka på **Ta bort** vid varje tjänstekatalog-fil du vill ersätta
3. Ladda upp ny tjänstekatalog via upload-området
4. AI-matchningen använder nu den uppdaterade katalogen

### Rensa temporära filer
Kör cleanup-scriptet regelbundet:
```bash
python clean_rag.py
```

### Återställa från backup
Om du behöver återställa RAG-databasen:
1. Stoppa servern
2. Ta bort `./chroma_db/` katalogen
3. Starta servern igen
4. Ladda upp dokument och tjänstekatalog på nytt

## Filstruktur

```
/home/frehal0707/use_cases/
├── clean_rag.py                    # Cleanup-script
├── chroma_db/                      # RAG vektordatabas
│   └── chroma.sqlite3
├── innovation_hub/
│   ├── api/
│   │   └── documents.py            # API endpoints
│   ├── ai/
│   │   └── rag_service.py          # RAG-service med delete-funktioner
│   └── frontend/
│       └── js/
│           └── documents.js        # GUI-funktioner
└── RAG_MANAGEMENT.md               # Denna fil
```

## API-dokumentation

Fullständig API-dokumentation finns på:
http://localhost:8000/docs

Sök efter "documents" för att hitta alla RAG-relaterade endpoints.

## Troubleshooting

### Filen syns i databasen men kan inte tas bort
- Kontrollera att filnamnet är exakt (case-sensitive)
- Använd URL-encoding för specialtecken

### Gamla filer dyker upp efter borttagning
- ChromaDB är persistent - ändringarna sparas direkt
- Ingen cachning - uppdatera sidan i browsern

### Kan inte ladda upp stora filer
- Max storlek: 10MB per fil
- För större filer, överväg att chunka dem manuellt

---

*Skapad: 2025-10-08*
*Status: Production-ready*

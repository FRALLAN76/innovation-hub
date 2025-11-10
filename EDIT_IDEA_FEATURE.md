# Redigera Idéer - Dokumentation

## Översikt
Du kan nu redigera befintliga idéer och automatiskt köra om AI-analysen för att få uppdaterade rekommendationer.

## Hur man använder

### Via Web-gränssnitt

1. **Gå till "Bläddra Idéer"-fliken**
   - http://localhost:8000 → Klicka på "Bläddra Idéer"

2. **Hitta idén du vill redigera**
   - Använd filter och sök för att hitta rätt idé

3. **Klicka på "Redigera"-knappen**
   - Finns längst till höger på varje idé-kort
   - Öppnar en modal med redigeringsformulär

4. **Uppdatera informationen**
   - **Titel**: Ändra titel
   - **Beskrivning**: Ändra beskrivning
   - **Typ**: Idé / Problem / Behov / Förbättring
   - **Målgrupp**: Medborgare / Företag / Medarbetare / Andra organisationer
   - **Kör AI-analys igen**: Checkboxen (förvald)

5. **Spara ändringar**
   - Klicka på "Spara ändringar"
   - Om "Kör AI-analys igen" är ikryssad:
     - AI kategoriserar om idén
     - Genererar nya taggar
     - Uppdaterar prioritet
     - Kör service mapping på nytt
     - Uppdaterar tjänsterekommendation

## Funktioner

### ✅ Vad uppdateras vid omanalys:

**AI-analys:**
- Kategori (Digital transformation, Medborgarservice, etc.)
- Prioritet (låg, medel, hög)
- AI-genererade taggar
- Sentiment-analys
- AI-tillförlitlighet

**Service Mapping:**
- Tjänsterekommendation (befintlig/utveckla/ny)
- Matchande tjänster från katalogen
- Matchningspoäng (0-100%)
- Utvecklingspåverkan (low/medium/high)
- Resonemang för rekommendation

**Bevaras:**
- Befintliga manuellt tillagda taggar
- Status (om AI-tillförlitlighet är låg)
- Skapare och skapelsedatum
- Kommentarer

### 🚀 Exempel på användning

#### Scenario: Förbättra beskrivningen
Du har lämnat in en idé med en kort beskrivning. Efter feedback vill du utöka den:

1. **Innan:**
   - Titel: "Digital parkerings-app"
   - Beskrivning: "En app för parkering"
   - Service recommendation: `None`

2. **Redigera:**
   - Behåll titel
   - Ny beskrivning: "En intelligent app där medborgare kan hitta och betala för parkering i realtid, med AI-optimering av lediga platser och integration med kommunens parkeringssystem."
   - ✅ Kör AI-analys igen

3. **Efter omanalys:**
   - Kategori: Digital transformation
   - Prioritet: Hög
   - Nya taggar: parkering, realtid, ai-optimering, betallösning
   - Service recommendation: `new_service` (80% confidence)
   - Matchande tjänster: 5 relaterade tjänster identifierade

## API-användning

### Uppdatera en idé
```bash
PUT /api/ideas/{idea_id}
Content-Type: application/json

{
  "title": "Uppdaterad titel",
  "description": "Uppdaterad beskrivning",
  "type": "idé",
  "target_group": "medborgare"
}
```

### Kör omanalys
```bash
POST /api/ideas/{idea_id}/analyze
```

**Returnerar:** Uppdaterad idé med ny AI-analys och service mapping

**Tidsåtgång:** ~30-60 sekunder (beroende på AI-responstid)

### Komplett exempel
```bash
# 1. Uppdatera idén
curl -X PUT "http://localhost:8000/api/ideas/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "AI-chatbot för medborgartjänster - Förbättrad",
    "description": "En intelligent chatbot med maskininlärning som kan svara på medborgares frågor dygnet runt.",
    "type": "idé",
    "target_group": "medborgare"
  }'

# 2. Kör omanalys
curl -X POST "http://localhost:8000/api/ideas/1/analyze"
```

## Vanliga frågor

### Varför tar omanalysen så lång tid?
- AI-analys via Qwen3 32B: ~10-20 sekunder
- RAG-baserad service mapping: ~10-20 sekunder
- Totalt: ~30-60 sekunder

### Kan jag stänga av omanalysen?
Ja, avmarkera checkboxen "Kör AI-analys igen" innan du sparar. Då uppdateras bara fälten du ändrat.

### Vad händer om AI-analysen misslyckas?
Idén sparas ändå med dina ändringar, men du får ett felmeddelande att omanalysen misslyckades.

### Försvinner mina manuella ändringar?
Nej, endast följande uppdateras av AI:n:
- Kategori
- Prioritet (om ändringsförslag finns)
- Status (endast vid mycket hög AI-tillförlitlighet >80%)
- Nya taggar läggs till (befintliga bevaras)
- Service mapping-data

Titel, beskrivning, typ och målgrupp kommer från ditt formulär.

### Kan jag återställa gamla värden?
För närvarande finns ingen ångra-funktion. Rekommendation: Kopiera viktiga fält innan du redigerar.

## Tekniska detaljer

### Flöde
```
1. Användare klickar "Redigera"
   ↓
2. Modal öppnas med befintlig data
   ↓
3. Användare ändrar fält
   ↓
4. Formulär skickas (PUT /api/ideas/{id})
   ↓
5. Idé uppdateras i databas
   ↓
6. [Om omanalys vald] POST /api/ideas/{id}/analyze
   ↓
7. AI-analys körs (kategori, prioritet, taggar, sentiment)
   ↓
8. Service mapping körs (RAG-baserad matchning)
   ↓
9. Resultat sparas i databas
   ↓
10. Modal stängs och listan uppdateras
```

### Felhantering
- Timeout: 60 sekunder (kan ändras i konfiguration)
- Nätverksfel: Visar felmeddelande, idé sparas inte
- AI-fel: Idé sparas, men omanalys misslyckades
- Valideringsfel: Visar vilket fält som är felaktigt

## Säkerhet

### Behörigheter
För närvarande kan alla användare redigera alla idéer. I framtiden:
- Endast skapare kan redigera sina egna idéer
- Administratörer kan redigera alla idéer
- SSO-integration för autentisering

### Auditlogg
För närvarande loggas:
- Uppdateringar i databas-timestamp
- AI-analys i serverloggar

Framtida förbättringar:
- Versionshistorik för idéer
- Ändringslogg synlig för användare
- Återställ till tidigare version

## Prestandaoptimering

### Nuvarande
- Omanalys: ~30-60 sekunder
- Caching: Ingen

### Planerade förbättringar
1. **Cachning av RAG-sökningar**
   - Spara tidigare service mappings för liknande idéer

2. **Parallellisering**
   - Kör AI-analys och service mapping samtidigt

3. **Inkrementell analys**
   - Endast omanalysera det som ändrats
   - Om bara titel ändrats → Mindre analys

4. **Bakgrundsprocessering**
   - Returnera direkt till användaren
   - Kör analys i bakgrunden
   - Notifiera när klar

---

*Implementerat: 2025-10-08*
*Status: Production-ready*
*API-version: 1.0.0*

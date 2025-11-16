# Payton Aandelenanalyse - Code Uitleg

## Wat doet deze applicatie?

De Payton Stock Analyzer is een Python-programma dat aandelengegevens analyseert en belangrijke financiële metrics berekent. Het helpt beleggers om aandelen te evalueren op basis van rendement, risico en groei.

---

## Gegevensstructuur: De Stock klasse

### Wat is een `Stock` object?

Een `Stock` is een gegevensstructuur (dataclass) die alle informatie over één aandeel opslaat:

```python
@dataclass
class Stock:
    bedrijf: str              # Bedrijfsnaam (bijv. "Apple")
    sector: str               # Bedrijfstak (bijv. "Technologie")
    koers: float              # Huidige aandelenkoers in euro
    eps: float                # Earnings Per Share (winst per aandeel)
    dividend: float           # Dividend dat het bedrijf uitkeert
    groei_percentage: float   # Verwachte groei in procenten
    risico: float             # Risicoscore (hoe hoger, des te riskanter)
```

### Berekende velden

Na het laden van de data berekent het programma twee extra waarden voor elke aandeel:

```python
    roi: float                # Return on Investment (rendement)
    valuatie_index: float     # Valuatie-index (waarderingsmaat)
```

---

## Formules: Hoe worden waarden berekend?

### 1. Return on Investment (ROI)

```
ROI = ((EPS + Dividend) / Koers) × 100
```

**Wat betekent dit?**
- We tellen de winst per aandeel (EPS) en dividend op
- We delen dit door de huidige aandelenkoers
- We vermenigvuldigen met 100 om het als percentage uit te drukken

**Voorbeeld:**
- Bedrijf: Apple
- EPS = 6.2 euro
- Dividend = 0.92 euro
- Koers = 150 euro

ROI = ((6.2 + 0.92) / 150) × 100 = (7.12 / 150) × 100 = 4.75%

Dit betekent dat je 4.75% rendement krijgt op je investering.

### 2. Valuatie-Index (Valuation Index)

```
Valuatie-Index = (ROI × Groei%) / Risico
```

**Wat betekent dit?**
- We vermenigvuldigen het rendement (ROI) met het groeipercentage
- We delen door de risicoscore
- Een hogere index = betere waardering

**Voorbeeld:**
- ROI = 4.75%
- Groei = 8.5%
- Risico = 5.2

Valuatie-Index = (4.75 × 8.5) / 5.2 = 40.375 / 5.2 = 7.76

---

## De StockAnalyzer klasse

### Initialisatie

```python
analyzer = StockAnalyzer(min_valuatie_index=10.0, max_risico=5.0)
```

Dit maakt een analyzer aan met filterinstellingen:
- **min_valuatie_index=10.0**: Toon alleen aandelen met valuatie-index ≥ 10
- **max_risico=5.0**: Toon alleen aandelen met risicoscore ≤ 5

### Functie 1: CSV inladen - `load_from_csv()`

```python
analyzer.load_from_csv('aandelen.csv')
```

**Wat doet deze functie?**

1. Opent het CSV-bestand `aandelen.csv`
2. Leest elke rij (elk aandeel)
3. Converteert tekstwaarden naar getallen (floats)
4. Creëert voor elk aandeel een `Stock` object
5. Roept `calculate_metrics()` aan om ROI en valuatie-index te berekenen
6. Slaat alles op in `self.stocks` lijst

**Foutafhandeling:**
- Controleert of het bestand bestaat
- Valideert dat alle vereiste kolommen aanwezig zijn
- Waarschuwt voor ongeldige rijen (bijv. negatieve koers)
- Slaat foutieve rijen over en gaat verder

### Functie 2: Filteren - `filter_stocks()`

```python
gefilterde_aandelen = analyzer.filter_stocks()
```

**Wat doet deze functie?**

1. Gaat door alle geladen aandelen
2. Behoudt alleen aandelen die aan beide criteria voldoen:
   - `valuatie_index >= min_valuatie_index`
   - `risico <= max_risico`
3. Sorteert de resultaten van hoog naar laag op valuatie-index
4. Retourneert de gefilterde lijst

**Voorbeeld:**
- Als we 15 aandelen laden en 6 voldoen aan de criteria
- Dan retourneert deze functie 6 aandelen, gesorteerd op beste valuatie-index eerst

### Functie 3: Rapport genereren - `generate_report()`

```python
rapport = analyzer.generate_report()
```

**Wat doet deze functie?**

1. Haalt de gefilterde aandelen op
2. Creëert een mooi geformatteerd tekstrapport met:
   - Titel en divider-lijnen
   - Filter-instellingen
   - Aantal aandelen (totaal en gefilterd)
   - Tabel met alle gefilterde aandelen
   - Voor elk aandeel: bedrijf, sector, koers, EPS, ROI, groei, risico, valuatie-index

**Voorbeeld output:**
```
============================================================
PAYTON - RAPPORT AANDELENANALYSE
============================================================

Filtercriteria:
  - Minimale valuatie-index: 10.0
  - Maximale risicoscore: 5.0
  - Totale aandelen geanalyseerd: 13
  - Aandelen die criteria vervullen: 6

------------------------------------------------------------
Bedrijf              Sector          Koers      EPS        ROI %      ...
------------------------------------------------------------
AVGO                 Technologie     180.00     7.45       4.14       ...
GOOG                 Technologie     140.00     4.73       3.38       ...
...
```

### Functie 4: Exporteren - `export_to_csv()`

```python
analyzer.export_to_csv('gefilterde_resultaten.csv')
```

**Wat doet deze functie?**

1. Haalt de gefilterde aandelen op
2. Opent een nieuw CSV-bestand voor schrijven
3. Schrijft alle kolommen naar het bestand:
   - Originele gegevens (bedrijf, sector, koers, etc.)
   - Berekende waarden (ROI, valuatie-index)
4. Slaat het bestand op

Dit is handig om de resultaten later verder te verwerken in Excel of andere tools.

---

## Hoe alles samen werkt

### Stap-voor-stap proces

```
1. START
   ↓
2. Creëer StockAnalyzer met filtercriteria
   ↓
3. Laad aandelen uit CSV-bestand
   ├─ Voor elk aandeel:
   │  ├─ Lees gegevens
   │  ├─ Bereken ROI
   │  └─ Bereken valuatie-index
   ↓
4. Filter aandelen volgens criteria
   ├─ Houd alleen goede aandelen
   └─ Sorteer op valuatie-index
   ↓
5. Genereer rapport
   ├─ Formatteer mooi
   └─ Print naar scherm
   ↓
6. Exporteer naar CSV (optioneel)
   ↓
7. EINDE
```

### Voorbeeld: Volledige uitvoering

```python
# 1. Creëer analyzer
analyzer = StockAnalyzer(min_valuatie_index=10.0, max_risico=5.0)

# 2. Laad gegevens
analyzer.load_from_csv('aandelen.csv')
# Resultaat: 13 aandelen geladen

# 3. Genereer en print rapport
analyzer.print_report()
# Resultaat: Toont 6 aandelen die criteria vervullen

# 4. Exporteer resultaten
analyzer.export_to_csv('gefilterde_resultaten.csv')
# Resultaat: Nieuw bestand aangemaakt
```

---

## CSV-bestandsformaat

### Input (aandelen.csv)

Het inputbestand gebruikt **puntkomma's** als scheidingsteken:

```csv
bedrijf;sector;koers;winst_per_aandeel;dividend;groei_percentage;risico
TechNova;Technologie;84.5;6.2;1.2;8.5;5.2
GreenPower;Energie;62.3;4.8;1.0;6.0;4.0
MediHealth;Gezondheid;97.8;7.1;2.1;9.0;4.5
```

### Output (gefilterde_resultaten.csv)

Het outputbestand bevat alle originele velden PLUS berekende waarden:

```csv
bedrijf;sector;koers;winst_per_aandeel;dividend;groei_percentage;risico;roi;valuatie_index
TechNova;Technologie;84.50;6.20;1.20;8.50;5.20;8.52;13.01
```

---

## Foutafhandeling

Het programma is voorzien van robuuste foutafhandeling:

### Bestandsfouten
```python
if not analyzer.load_from_csv('aandelen.csv'):
    print("Fout: Bestand niet gevonden of geladen")
```

### Validatiefouten
- Controleert of alle vereiste kolommen aanwezig zijn
- Valideert dat koers > 0
- Converteert waarden veilig naar getallen

### Deling door nul
```python
if self.risico > 0:
    self.valuatie_index = (self.roi * self.groei_percentage) / self.risico
else:
    self.valuatie_index = 0.0  # Standaard waarde
```

---

## Parameteroptimalisatie

Je kunt de filters aanpassen op basis van je strategie:

### Conservatief (lage risico)
```python
analyzer = StockAnalyzer(
    min_valuatie_index=15.0,  # Hogere minimale index
    max_risico=3.0             # Lager maximaal risico
)
```

### Agressief (hoger rendement)
```python
analyzer = StockAnalyzer(
    min_valuatie_index=5.0,   # Lagere minimale index
    max_risico=5.5             # Hoger maximaal risico
)
```

---

## Samenvatting

| Onderdeel | Functie | Input | Output |
|-----------|---------|-------|--------|
| Stock klasse | Opslag van aandeel-gegevens | Individuele waarden | Stock object |
| load_from_csv() | Inladen van CSV-bestand | Bestandsnaam | Gevulde stocks lijst |
| calculate_metrics() | Berekening ROI en index | Stock gegevens | ROI en valuatie_index |
| filter_stocks() | Filteren op criteria | Stocks lijst | Gefilterde en gesorteerde lijst |
| generate_report() | Rapport-generering | Gefilterde stocks | Geformatteerde string |
| export_to_csv() | Opslaan resultaten | Gevensleegde stocks | CSV-bestand |

---

## Voordelen van deze aanpak

✅ **Modulair**: Elk onderdeel heeft één verantwoordelijkheid
✅ **Herbruikbaar**: De klasses kunnen in andere programma's gebruikt worden
✅ **Schaalbaar**: Werkt met 10 of 10.000 aandelen
✅ **Veilig**: Goede foutafhandeling
✅ **Flexibel**: Filters kunnen aangepast worden
✅ **Documenteerd**: Duidelijke docstrings en type hints


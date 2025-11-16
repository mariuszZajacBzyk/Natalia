# Payton Stock Analysis Application

Een Python-gebaseerde toepassing voor het analyseren van aandelenprestaties met behulp van financiële meetgegevens.

## Functies

- **Inladen van CSV-bestanden** met aandelengegevens
- **Berekening van financiële metrics**:
  - Earnings Per Share (EPS)
  - Return on Investment (ROI)
  - Valuation Index
- **Filtering en sortering** op basis van gebruikerscriteria
- **Exporteren van resultaten** naar CSV
- **Gedetailleerde rapportage** in console

## Formules

### 1. Return on Investment (ROI)
```
ROI = ((EPS + Dividend) / Price) × 100
```

### 2. Valuation Index
```
Index = (ROI × Growth Percentage) / Risk Score
```

## Vereisten

- Python 3.6 of hoger
- Geen externe bibliotheken nodig (alleen standaardbibliotheek)

## Gebruik

### Basis gebruik
```bash
python3 stock_analyzer.py sample_stocks.csv
```

### Met aangepaste filterparameters
```bash
python3 stock_analyzer.py sample_stocks.csv -m 15 -r 4
```

### Met export naar CSV
```bash
python3 stock_analyzer.py sample_stocks.csv -o results.csv
```

## Opdrachtregelparameters

- `input_csv` (verplicht): Pad naar de input CSV-bestand
- `-o, --output`: Pad voor de output CSV-bestand met gefilterde resultaten
- `-m, --min-index`: Minimale valuation index (standaard: 10.0)
- `-r, --max-risk`: Maximale risk score (standaard: 5.0)

## CSV-invoerindeling

Het invoer-CSV-bestand moet de volgende kolommen bevatten:

| Kolom | Type | Beschrijving |
|-------|------|-------------|
| symbol | string | Aandelensymbool (bijv. AAPL) |
| name | string | Bedrijfsnaam |
| price | float | Huidige aandelenkoers |
| earnings | float | Totale inkomsten |
| dividend | float | Dividend per aandeel (optioneel, standaard: 0.0) |
| growth_percentage | float | Groeipercentage (optioneel, standaard: 0.0) |
| risk_score | float | Risicoscore (optioneel, standaard: 1.0) |

### Voorbeeld invoer-CSV
```csv
symbol,name,price,earnings,dividend,growth_percentage,risk_score
AAPL,Apple Inc.,150.00,5.61,0.92,12.5,2.3
MSFT,Microsoft Corporation,320.00,9.20,0.68,15.0,2.1
```

## Filterlogica

De toepassing filtert aandelen op basis van:
1. **Minimale Valuation Index**: Toont alleen aandelen met `valuation_index >= minimum`
2. **Maximale Risicoscore**: Toont alleen aandelen met `risk_score <= maximum`

Resultaten worden **aflopend gesorteerd** op valuation index (hoogste eerst).

## Voorbeeld

```bash
$ python3 stock_analyzer.py sample_stocks.csv -m 10 -r 5

====================================================================================================
STOCK ANALYSIS REPORT - Payton
====================================================================================================

Filter Criteria:
  - Minimum Valuation Index: 10.0
  - Maximum Risk Score: 5.0
  - Total stocks analyzed: 15
  - Stocks meeting criteria: 6

----------------------------------------------------------------------------------------------------
Symbol   Name                      Price      EPS        ROI %      Growth %   Risk     Valuation   
----------------------------------------------------------------------------------------------------
AVGO     Broadcom Inc.             180.00     7.45       4.14       20.00      2.70     30.66       
GOOG     Alphabet Inc.             140.00     4.73       3.38       18.00      2.50     24.33       
AAPL     Apple Inc.                150.00     5.61       4.35       12.50      2.30     23.66       
MSFT     Microsoft Corporation     320.00     9.20       3.09       15.00      2.10     22.05       
QCOM     Qualcomm Inc.             180.00     4.89       2.72       16.00      3.00     14.49       
INTC     Intel Corporation         35.00      1.54       7.23       8.00       4.20     13.77       
----------------------------------------------------------------------------------------------------

Report exported to filtered_results.csv
```

## Uitvoergegevens

De gefilterde resultaten worden geëxporteerd met alle berekende metriek:

| Kolom | Beschrijving |
|-------|-------------|
| symbol | Aandelensymbool |
| name | Bedrijfsnaam |
| price | Aandelenkoers |
| earnings | Totale inkomsten |
| dividend | Dividend per aandeel |
| growth_percentage | Groeipercentage |
| risk_score | Risicoscore |
| eps | Berekende Earnings Per Share |
| roi | Berekende Return on Investment (%) |
| valuation_index | Berekende valuatiebeurlijst |

## Foutafhandeling

De toepassing:
- Valideert invoergegevens en rapporteert waarschuwingen voor ongeldige rijen
- Controleert of vereiste CSV-kolommen aanwezig zijn
- Verwerkt ontbrekende gegevens met standaardwaarden
- Voorkomt divisie door nul in berekeningen

## Licentie

Dit project is beschikbaar onder de MIT-licentie.

# Masterarbeit: Performance- und Nutzbarkeitsvergleich von k-Anonymisierung (Samarati) in Python und AWS Lambda

## Projektbeschreibung

Dieses Projekt untersucht die k-Anonymisierung nach dem Samarati-Ansatz und vergleicht die Performance sowie die Nutzbarkeit einer lokalen Python-Implementierung mit zwei Varianten einer AWS Lambda Implementierung.

Ziel der Arbeit ist es, herauszufinden, welche Implementierung effizienter und benutzerfreundlicher ist, insbesondere im Kontext von großen Patientendatensätzen und komplexen Generalisierungshierarchien.

## Motivation

k-Anonymisierung ist eine weit verbreitete Technik zum Schutz von personenbezogenen Daten, insbesondere im medizinischen Bereich. Während lokale Implementierungen einfach zu entwickeln und zu testen sind, bieten Cloud-basierte Lösungen wie AWS Lambda eine potenziell bessere Skalierbarkeit und Performance.

Dieses Projekt vergleicht:

- **Lokale Implementierung**: Basierend auf einem Fork von [data-privacy](https://github.com/ltzheng/data-privacy).
- **AWS Lambda Implementierungen**:
  - **AWS-V1**: Mit einer normalen Map und minimalem Einsatz von S3.
  - **AWS-V2**: Mit einer DistributedMap zur Unterstützung von mehr Quasi-Identifikatoren und größeren Patientendatensätzen.

## Projektstruktur

```plaintext
.
├── Code
│   ├── Lokal          # Lokale Python Implementierung (geforkt und adaptiert)
│   └── AWS
│       ├── V1         # Erste AWS-Implementierung mit normaler Map und wenig S3 Nutzung
│       └── V2         # Erweiterung mit DistributedMap für größere Datenmengen
│
├── Input
│   ├── Generalization # Generalisierungshierarchien der Quasi-Identifier
│   └── Patients       # CSV-Dateien mit Patientendaten
│
└── Output
    ├── Dataframes     # Ergebnisdaten aus Performance- und Nutzbarkeitsvergleich
    ├── Plot           # Visualisierung der Performance- und Nutzbarkeitsdaten
    └── Tabelle        # Beispiele anonymisierter Tabellen
```

## Implementierungsdetails

### 1. Lokale Implementierung
- Basierend auf einem Fork des Repos [data-privacy](https://github.com/ltzheng/data-privacy)
- Anpassungen zur Unterstützung der Generalisierungshierarchien und zur Auswertung von Performance und Nutzbarkeit

### 2. AWS Implementierungen
- **AWS-V1**:
  - Verwendung einer normalen Map zur Datenverarbeitung
  - Minimale Nutzung von S3 zur Datenspeicherung
  - Fokus auf Einfachheit und schnelle Umsetzung
- **AWS-V2**:
  - Einsatz einer DistributedMap zur Parallelisierung und Skalierung
  - Bessere Unterstützung für mehr Quasi-Identifier und größere Patientendatensätze
  - Optimierte Nutzung von S3 für Input und Output

## Inputdaten

- **Patients**: CSV-Dateien mit Patientendaten, die für die k-Anonymisierung verwendet werden.
- **Generalization**: Generalisierungshierarchien der Quasi-Identifier (z.B. Alter, PLZ, Geschlecht).

## Outputdaten

- **Dataframes**: Daten, die aus dem Performance- und Nutzbarkeitsvergleich resultieren.
- **Plot**: Visualisierte Ergebnisse zur besseren Interpretation der Performance- und Nutzbarkeitsdaten.
- **Tabelle**: Beispiele anonymisierter Tabellen, die aus den verschiedenen Implementierungen resultieren.

## Ergebnisse und Auswertung

Die Ergebnisse der Arbeit sind in Form von Dataframes und Visualisierungen im Ordner `Output` zu finden. Die Auswertung umfasst:
- Performance-Vergleich der lokalen Implementierung und der beiden AWS-Varianten.
- Vergleich der Nutzbarkeit hinsichtlich Skalierbarkeit, Flexibilität und Benutzerfreundlichkeit.
- Beispiele anonymisierter Tabellen zur Veranschaulichung der Datenveränderung.

## Voraussetzungen

- Python 3.x
- AWS Account mit Berechtigungen für Lambda und S3
- Abhängigkeiten aus `requirements.txt` (im Ordner `Code`)

## Installation und Ausführung

### Lokale Implementierung
```bash
cd Code/Lokal
pip install -r requirements.txt
python main.py
```

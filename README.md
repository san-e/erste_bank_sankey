# erste_bank_sankey
Generiert Sankey-Diagramme aus monatlichen George-Kontoauszügen im JSON-Format.

## Setup
```bash
git clone https://github.com/san-e/erste_bank_sankey
cd erste_bank_sankey
uv sync
```

## Benutzung
1. Alle gewünschten monatlichen (!) Kontoauszüge aus George im JSON-Format runterladen und in den `kontoauszüge` Ordner verschieben.
2. ```bash
   uv run main.py
   ```
3. Die generierten .svg Dateien werden im Ordner `sankeys` abgelegt.


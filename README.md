# Invoice Analyzer System

Brazilian Electronic Service Invoice (NFS-e) analysis system for Alfa Entretenimento S/A.

## Features

- 📄 PDF Invoice Analysis
- 🏛️ Multi-state Support (SP, RJ, MG, BA, PR, RS, SC, DF)
- 💰 Tax Calculation & Retention Detection
- 🎯 Confidence Scoring System
- 🌐 Web Interface with Drag & Drop
- 📊 Export Results to TXT

## Tech Stack

- **Backend**: Python 3.8+, Flask
- **PDF Processing**: PyPDF2, pdfplumber
- **Frontend**: HTML5, CSS3, JavaScript
- **UI**: Glassmorphism design with Alfa branding

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Alfa-Entretenimento/invoice-analyzer.git
cd invoice-analyzer
```

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask server:
```bash
python app.py
```

2. Open browser at `http://localhost:5001`

3. Upload PDF invoice via drag & drop or file selection

4. View analysis results and export if needed

## Project Structure

```
invoice-analyzer/
├── app.py                    # Flask application
├── analisador_nf_v2.py      # Invoice analyzer engine
├── requirements.txt         # Python dependencies
├── templates/
│   └── index.html          # Web interface
├── static/
│   ├── css/
│   │   └── style.css       # Alfa theme styles
│   └── js/
│       └── main.js         # Frontend logic
└── notas/                  # Sample invoices (optional)
```

## Supported Invoice Formats

The system automatically detects and processes invoices from:
- São Paulo (SP)
- Rio de Janeiro (RJ)
- Minas Gerais (MG)
- Bahia (BA)
- Paraná (PR)
- Rio Grande do Sul (RS)
- Santa Catarina (SC)
- Distrito Federal (DF)

## API Endpoints

- `GET /` - Main interface
- `POST /analyze` - Analyze PDF invoice
- `GET /sample` - Get sample data

## License

© 2024 Alfa Entretenimento S/A. All rights reserved.

## Support

For issues and support, contact the Alfa Entertainment development team.
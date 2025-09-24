# Pokémon Legends: Arceus – Pokedex Tracker

This project automates the process of identifying which Pokémon you have not yet captured in *Pokémon Legends: Arceus* by using OCR to read screenshots from your Pokédex. It also helps organize uncaught Pokémon by region and sub-location for efficient tracking and exploration.

## Features

- **Screenshot OCR** using Tesseract and PyTesseract
- **Master Pokédex Parsing** from guidebook data
- **Uncaught Pokémon Detection** based on your current caught list
- **Web Interface** to filter uncaught Pokémon by region and sub-location
- Built with Python (backend) and React + Vite + TailwindCSS (frontend)

## Directory Structure

```
Pokemon/
├── backend/
│   ├── scrape.py                # OCR-based caught Pokémon extractor
│   ├── master_pokedex.py        # Parses the full master Pokédex with locations
│   ├── uncaught_pokemon.py      # Compares caught vs master and creates uncaught list
│   ├── main.py                  # Runs scrape + uncaught generation
│   └── pokedex_status.json      # Auto-generated list of captured Pokémon
│   └── uncaught_pokemon.json    # Auto-generated list of uncaught Pokémon
│   └── mastered_pokedex.json    # Parsed full Pokédex with locations
├── frontend/
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── index.html
│   └── src/
│       └── App.jsx              # UI to display uncaught Pokémon by region
├── screenshots/                 # Folder for saved annotated screenshots
├── README.md
```

## Getting Started

### Backend Setup (Python)

1. **Create virtual environment**  
   ```bash
   python3 -m venv pokedex_env
   source pokedex_env/bin/activate
   ```

2. **Install dependencies**  
   ```bash
   pip install pyautogui pillow pytesseract opencv-python
   brew install tesseract  # on macOS
   ```

3. **Run the pipeline**
   ```bash
   python backend/main.py
   ```

---

### Frontend Setup (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173/` in your browser.

---

## GitHub Repository Description

> A Pokémon Legends: Arceus OCR-based tracker that detects uncaught Pokémon from your screenshots and displays them by region and sub-location on a web app.

# Sistema de Humor (Python)

Este projeto demonstra como ter a mesma lógica para Web (Flask) e Desktop (Tkinter).

## Estrutura
- core/: lógica compartilhada
- backend/: app Flask (rota `/` e `/api/humor?tipo=`)
- frontend/: HTML/CSS/JS da página
- desktop/: app Tkinter

## Como rodar (Web)
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
python backend/app.py
# Abrir http://localhost:5000
```

## Como rodar (Desktop)
```bash
python desktop/main.py
```

## Empacotar Desktop (opcional)
```bash
pip install pyinstaller
pyinstaller --onefile desktop/main.py
```


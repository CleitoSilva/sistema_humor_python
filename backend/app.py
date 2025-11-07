from flask import Flask, render_template, request, jsonify
from core.humor import obter_mensagem, inicializar_banco

# Cria o app Flask
app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

# Inicializa o banco (apenas uma vez)
inicializar_banco()

# ==========================
# ROTAS
# ==========================

@app.get("/")
def index():
    """Página inicial"""
    return render_template("index.html")

@app.get("/api/humor")
def api_humor():
    """Endpoint JSON para obter mensagem de humor"""
    tipo = request.args.get("tipo", "neutro")
    return jsonify(obter_mensagem(tipo))

# ==========================
# ENTRYPOINT
# ==========================
# A Vercel detecta o objeto `app` automaticamente.
# Esse bloco é apenas para execução local.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
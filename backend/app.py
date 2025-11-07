from flask import Flask, render_template, request, jsonify
from core.humor import obter_mensagem

app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/api/humor")
def api_humor():
    tipo = request.args.get("tipo", "neutro")
    return jsonify(obter_mensagem(tipo))

if __name__ == "__main__":
    app.run(debug=True)

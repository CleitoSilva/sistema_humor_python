# core/humor.py
import sqlite3
import calendar
from dataclasses import dataclass
from datetime import date

# Caminho do banco de dados
DB_PATH = "data.sqlite"

# ==========================
# 1️⃣ MODELO DE DADOS
# ==========================
@dataclass
class RegistroHumor:
    data: str   # YYYY-MM-DD
    humor: str  # "feliz", "neutro", "triste"
    anotacao: str = ""

# ==========================
# 2️⃣ BANCO DE DADOS
# ==========================
def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def inicializar_banco():
    with conectar() as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS registros (
            data TEXT PRIMARY KEY,
            humor TEXT NOT NULL,
            anotacao TEXT DEFAULT ''
        );
        """)
        con.commit()

# ==========================
# 3️⃣ OPERAÇÕES PRINCIPAIS
# ==========================
def salvar_humor(data_str: str, humor: str, anotacao: str = ""):
    """Insere ou atualiza o humor de um dia."""
    with conectar() as con:
        con.execute("""
        INSERT INTO registros (data, humor, anotacao)
        VALUES (?, ?, ?)
        ON CONFLICT(data) DO UPDATE SET
            humor = excluded.humor,
            anotacao = excluded.anotacao;
        """, (data_str, humor, anotacao))
        con.commit()

def obter_humor(data_str: str) -> RegistroHumor | None:
    """Busca o registro de um dia específico."""
    with conectar() as con:
        row = con.execute("SELECT * FROM registros WHERE data = ?", (data_str,)).fetchone()
        if row:
            return RegistroHumor(row["data"], row["humor"], row["anotacao"])
        return None

def listar_mes(ano: int, mes: int) -> list[RegistroHumor]:
    """Lista todos os registros de um mês."""
    prefixo = f"{ano:04d}-{mes:02d}-"
    with conectar() as con:
        rows = con.execute("SELECT * FROM registros WHERE data LIKE ? ORDER BY data", (prefixo + "%",)).fetchall()
        return [RegistroHumor(r["data"], r["humor"], r["anotacao"]) for r in rows]

def estatisticas() -> dict:
    """Conta quantos dias feliz/neutro/triste."""
    with conectar() as con:
        rows = con.execute("SELECT humor, COUNT(*) as total FROM registros GROUP BY humor").fetchall()
        resultado = {"feliz": 0, "neutro": 0, "triste": 0}
        for r in rows:
            resultado[r["humor"]] = r["total"]
        return resultado

def calendario_mes(ano: int, mes: int) -> list[list[dict]]:
    """Retorna uma matriz de semanas para o calendário mensal."""
    cal = calendar.Calendar(firstweekday=0)
    dias = {r.data: r.humor for r in listar_mes(ano, mes)}
    semanas = []
    for semana in cal.monthdatescalendar(ano, mes):
        linha = []
        for d in semana:
            if d.month != mes:
                linha.append({"data": None, "humor": None})
            else:
                linha.append({"data": d.isoformat(), "humor": dias.get(d.isoformat())})
        semanas.append(linha)
    return semanas

# ==========================
# 4️⃣ INICIALIZAÇÃO AUTOMÁTICA
# ==========================
inicializar_banco()
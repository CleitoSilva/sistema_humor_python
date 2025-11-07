import tkinter as tk
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))


import customtkinter as ctk
from tkinter import messagebox
from datetime import date
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import calendar
from core.humor import salvar_humor, obter_humor, estatisticas, listar_mes


# ===============================
# CONFIGURAÇÕES BÁSICAS
# ===============================
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

hoje = date.today()
humor_atual = "neutro"

TEMAS_HUMOR = {
    "feliz":  {"cor": "#60A5FA", "emoji": "😀", "texto": "Feliz"},
    "neutro": {"cor": "#E5E7EB", "emoji": "😐", "texto": "Neutro"},
    "triste": {"cor": "#F87171", "emoji": "😢", "texto": "Triste"},
}

# Atividades
atividades = {
    "exercicio": False, "sono": False, "social": False,
    "alimentacao": False, "trabalho": False,
}
cores_atividades = {
    "exercicio": {"ativa": "#22C55E", "inativa": "#A7F3D0"},
    "sono": {"ativa": "#3B82F6", "inativa": "#BFDBFE"},
    "social": {"ativa": "#FACC15", "inativa": "#FEF9C3"},
    "alimentacao": {"ativa": "#F97316", "inativa": "#FED7AA"},
    "trabalho": {"ativa": "#8B5CF6", "inativa": "#E9D5FF"},
}
icons = {
    "exercicio": "🏃‍♂️ Exercício", "sono": "💤 Sono",
    "social": "💬 Social", "alimentacao": "🍎 Alimentação",
    "trabalho": "💻 Trabalho",
}

# ===============================
# FUNÇÕES
# ===============================
def desenhar_gradiente(canvas, cor1="#93C5FD", cor2="#C7D2FE"):
    canvas.delete("all")
    largura, altura = max(1, canvas.winfo_width()), max(1, canvas.winfo_height())
    steps = 120
    r1, g1, b1 = [int(cor1[i:i+2], 16) for i in (1, 3, 5)]
    r2, g2, b2 = [int(cor2[i:i+2], 16) for i in (1, 3, 5)]
    for i in range(steps):
        r = int(r1 + (r2 - r1) * i / steps)
        g = int(g1 + (g2 - g1) * i / steps)
        b = int(b1 + (b2 - b1) * i / steps)
        cor = f"#{r:02x}{g:02x}{b:02x}"
        y1, y2 = int(altura * i / steps), int(altura * (i + 1) / steps)
        canvas.create_rectangle(0, y1, largura, y2, outline="", fill=cor)

def atualizar_humor(novo_humor):
    global humor_atual
    humor_atual = novo_humor if novo_humor in TEMAS_HUMOR else "neutro"
    tema = TEMAS_HUMOR[humor_atual]
    lbl_emoji.configure(text=tema["emoji"])
    lbl_status.configure(text=f"Hoje você está {tema['texto']}")
    desenhar_gradiente(bg_canvas, tema["cor"], "#C7D2FE")

def alternar_atividade(nome):
    atividades[nome] = not atividades[nome]
    ativo = atividades[nome]
    btn = botoes_atividades[nome]
    btn.configure(
        fg_color=cores_atividades[nome]["ativa" if ativo else "inativa"],
        hover_color=cores_atividades[nome]["ativa"]
    )

def confirmar_dia():
    nota = txt_nota.get("0.0", "end").strip()
    extras = ", ".join([rotulo for chave, rotulo in icons.items() if atividades[chave]])
    if extras:
        nota = (nota + ("\n" if nota else "")) + f"Atividades: {extras}"
    salvar_humor(hoje.isoformat(), humor_atual, nota)
    atualizar_estatisticas()
    atualizar_grafico()
    atualizar_calendario()
    messagebox.showinfo("Dia confirmado", f"✅ Seu dia foi salvo!\nHumor: {humor_atual.upper()}")

def carregar():
    registro = obter_humor(hoje.isoformat())
    if registro:
        atualizar_humor(registro.humor)
        txt_nota.delete("0.0", "end")
        txt_nota.insert("0.0", registro.anotacao)

def atualizar_estatisticas():
    s = estatisticas()
    lbl_stats.configure(text=f"😀 Feliz: {s['feliz']}   😐 Neutro: {s['neutro']}   😢 Triste: {s['triste']}")

# ===============================
# INTERFACE
# ===============================
app = ctk.CTk()
app.title("Mood Tracker Deluxe")
app.geometry("950x750")

bg_canvas = tk.Canvas(app, highlightthickness=0, bd=0)
bg_canvas.pack(fill="both", expand=True)
bg_canvas.bind("<Configure>", lambda e: desenhar_gradiente(bg_canvas))

main_frame = ctk.CTkFrame(bg_canvas, corner_radius=20, fg_color="white")
main_frame.place(relx=0.5, rely=0.48, anchor="center", relwidth=0.9, relheight=0.9)

frame_esquerda = ctk.CTkFrame(main_frame, fg_color="transparent")
frame_esquerda.pack(side="left", fill="both", expand=True, padx=(25, 10), pady=25)

frame_direita = ctk.CTkFrame(main_frame, fg_color="transparent", width=300)
frame_direita.pack(side="right", fill="y", padx=(10, 25), pady=25)

# ---- Conteúdo esquerdo
lbl_titulo = ctk.CTkLabel(frame_esquerda, text="Como você se sente hoje?", font=("Segoe UI", 22, "bold"))
lbl_titulo.pack(pady=(10, 10))

lbl_emoji = ctk.CTkLabel(frame_esquerda, text="😐", font=("Segoe UI Emoji", 90))
lbl_emoji.pack(pady=5)

lbl_status = ctk.CTkLabel(frame_esquerda, text="Hoje você está Neutro", font=("Segoe UI", 16))
lbl_status.pack(pady=(0, 15))

# Humor
frame_botoes = ctk.CTkFrame(frame_esquerda, fg_color="transparent")
frame_botoes.pack(pady=10)
btn_feliz = ctk.CTkButton(frame_botoes, text="😀 Feliz", width=110, height=38, fg_color="#60A5FA",
                          hover_color="#3B82F6", command=lambda: atualizar_humor("feliz"))
btn_neutro = ctk.CTkButton(frame_botoes, text="😐 Neutro", width=110, height=38, fg_color="#9CA3AF",
                           hover_color="#6B7280", command=lambda: atualizar_humor("neutro"))
btn_triste = ctk.CTkButton(frame_botoes, text="😢 Triste", width=110, height=38, fg_color="#F87171",
                           hover_color="#DC2626", command=lambda: atualizar_humor("triste"))
btn_feliz.grid(row=0, column=0, padx=6)
btn_neutro.grid(row=0, column=1, padx=6)
btn_triste.grid(row=0, column=2, padx=6)

# Atividades
lbl_atividades = ctk.CTkLabel(frame_esquerda, text="Atividades de hoje:", font=("Segoe UI", 15, "bold"))
lbl_atividades.pack(pady=(15, 8))
frame_atividades = ctk.CTkFrame(frame_esquerda, fg_color="transparent")
frame_atividades.pack(pady=5)

botoes_atividades = {}
for i, (chave, texto) in enumerate(icons.items()):
    btn = ctk.CTkButton(frame_atividades, text=texto, width=130, height=35,
                        fg_color=cores_atividades[chave]["inativa"],
                        hover_color=cores_atividades[chave]["ativa"],
                        command=lambda n=chave: alternar_atividade(n))
    btn.grid(row=0, column=i, padx=4, pady=3)
    botoes_atividades[chave] = btn

# Anotação compacta
lbl_nota = ctk.CTkLabel(frame_esquerda, text="Anotações do dia:", font=("Segoe UI", 14, "bold"))
lbl_nota.pack(pady=(15, 5))
txt_nota = ctk.CTkTextbox(frame_esquerda, width=500, height=50)
txt_nota.pack(pady=(0, 10))

btn_confirmar = ctk.CTkButton(
    frame_esquerda, text="✅ Confirmar Dia", width=180, height=40,
    font=("Segoe UI", 15, "bold"), fg_color="#1E3A8A",
    hover_color="#1E40AF", corner_radius=8, command=confirmar_dia
)
btn_confirmar.pack(pady=(10, 15))

# ---- Lado direito: gráfico + calendário
lbl_stats = ctk.CTkLabel(frame_direita, text="Resumo do Humor", font=("Segoe UI", 14, "bold"))
lbl_stats.pack(pady=(10, 5))

fig, ax = plt.subplots(figsize=(3.2, 3.2), facecolor="#ffffff")
canvas_grafico = FigureCanvasTkAgg(fig, master=frame_direita)
canvas_grafico.get_tk_widget().pack(pady=5)

def atualizar_grafico():
    s = estatisticas()
    ax.clear()
    valores = [max(0, s["feliz"]), max(0, s["neutro"]), max(0, s["triste"])]
    total = sum(valores)
    if total == 0:
        valores, autopct = [1, 1, 1], ""
    else:
        autopct = "%1.0f%%"
    ax.pie(valores, labels=["Feliz", "Neutro", "Triste"],
           colors=["#60A5FA", "#9CA3AF", "#F87171"],
           autopct=autopct, startangle=90,
           wedgeprops={"edgecolor": "white"}, textprops={"fontsize": 9})
    ax.axis("equal")
    canvas_grafico.draw()

# ===== CALENDÁRIO COLORIDO =====
lbl_cal = ctk.CTkLabel(frame_direita, text="Calendário do Humor", font=("Segoe UI", 14, "bold"))
lbl_cal.pack(pady=(15, 5))

frame_cal = ctk.CTkFrame(frame_direita, fg_color="#F9FAFB", corner_radius=10)
frame_cal.pack(pady=(0, 15), fill="x")

ano_atual = date.today().year
mes_atual = date.today().month
hoje = date.today()

def atualizar_calendario():
    """Atualiza o calendário do humor com base no mês/ano atual"""
    for widget in frame_cal.winfo_children():
        widget.destroy()

    global ano_atual, mes_atual

    registros = {r.data: r.humor for r in listar_mes(ano_atual, mes_atual)}
    cal = calendar.Calendar(firstweekday=0)

    # Cabeçalho com setas de navegação
    header_frame = ctk.CTkFrame(frame_cal, fg_color="transparent")
    header_frame.grid(row=0, column=0, columnspan=7, pady=(5, 5))

    btn_prev = ctk.CTkButton(header_frame, text="◀️", width=30, height=30,
                             fg_color="#E5E7EB", text_color="#111827",
                             hover_color="#D1D5DB", command=mes_anterior)
    btn_prev.pack(side="left", padx=10)

    lbl_mes = ctk.CTkLabel(header_frame,
                           text=f"{calendar.month_name[mes_atual]} {ano_atual}",
                           font=("Segoe UI", 13, "bold"))
    lbl_mes.pack(side="left", expand=True)

    btn_next = ctk.CTkButton(header_frame, text="▶️", width=30, height=30,
                             fg_color="#E5E7EB", text_color="#111827",
                             hover_color="#D1D5DB", command=mes_posterior)
    btn_next.pack(side="right", padx=10)

    # Dias da semana
    dias_semana = ["S", "T", "Q", "Q", "S", "S", "D"]
    for i, d in enumerate(dias_semana):
        ctk.CTkLabel(frame_cal, text=d, width=25,
                     fg_color="transparent", font=("Segoe UI", 12, "bold")).grid(row=1, column=i)

    linha = 2
    for semana in cal.monthdatescalendar(ano_atual, mes_atual):
        for col, dia in enumerate(semana):
            cor = "#F3F4F6"
            if dia.month == mes_atual:
                humor = registros.get(dia.isoformat())
                if humor:
                    cor = TEMAS_HUMOR[humor]["cor"]

                # Destaque do dia atual
                if dia == hoje:
                    dia_frame = ctk.CTkFrame(frame_cal, fg_color="#1E3A8A", corner_radius=10)
                    dia_frame.grid(row=linha, column=col, padx=2, pady=2)
                    ctk.CTkLabel(dia_frame, text=str(dia.day), width=25, fg_color=cor,
                                 corner_radius=6, text_color="white",
                                 font=("Segoe UI", 11, "bold")).pack(padx=2, pady=2)
                else:
                    ctk.CTkLabel(frame_cal, text=str(dia.day), width=25, fg_color=cor,
                                 corner_radius=6, text_color="white",
                                 font=("Segoe UI", 11)).grid(row=linha, column=col, padx=2, pady=2)
            else:
                ctk.CTkLabel(frame_cal, text="", width=25, fg_color="transparent").grid(row=linha, column=col)
        linha += 1


def mes_anterior():
    """Retrocede um mês no calendário"""
    global ano_atual, mes_atual
    mes_atual -= 1
    if mes_atual < 1:
        mes_atual = 12
        ano_atual -= 1
    atualizar_calendario()


def mes_posterior():
    """Avança um mês no calendário"""
    global ano_atual, mes_atual
    mes_atual += 1
    if mes_atual > 12:
        mes_atual = 1
        ano_atual += 1
    atualizar_calendario()


# Inicializa o calendário na primeira execução
atualizar_calendario()
        
# Botão atualizar gráfico
btn_atualizar_grafico = ctk.CTkButton(frame_direita, text="🔄 Atualizar gráfico",
                                      width=180, height=35, fg_color="#3B82F6",
                                      hover_color="#2563EB",
                                      command=lambda: [atualizar_estatisticas(), atualizar_grafico(), atualizar_calendario()])
btn_atualizar_grafico.pack(pady=(15, 5))

# Inicialização
atualizar_humor(humor_atual)
carregar()
atualizar_estatisticas()
atualizar_grafico()
atualizar_calendario()

app.mainloop()
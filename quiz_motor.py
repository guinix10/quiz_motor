import streamlit as st
import subprocess
import psutil

# ⚠️ DEVE SER A PRIMEIRA CHAMADA STREAMLIT
st.set_page_config(page_title="Quiz Motor 6 Fios", page_icon="⚙️", layout="centered")

# CSS
st.markdown("""
    <style>
    body, .stApp {
        background-color: #0d0d0d;
        color: #e0f7fa;
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3 {
        color: #00ffd5;
        text-align: center;
        text-shadow: 0 0 10px #00ffd5;
    }
    .stButton>button {
        background: linear-gradient(135deg, #00bfff, #007bff);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-size: 18px;
        margin: 10px 5px;
        box-shadow: 0 0 10px rgba(0, 191, 255, 0.5);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #007bff, #005bb5);
        transform: scale(1.05);
        box-shadow: 0 0 15px rgba(0, 191, 255, 0.8);
    }
    .st-expander {
        background-color: #1c1c1c !important;
        color: white !important;
        border-radius: 10px !important;
        border: 1px solid #333 !important;
    }
    .st-success {
        background-color: #14532d !important;
        border-left: 5px solid #22c55e !important;
    }
    .st-error {
        background-color: #7f1d1d !important;
        border-left: 5px solid #ef4444 !important;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 700px;
        margin: auto;
    }
    .pergunta-caixa {
        background-color: #1f1f1f;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #00ffd5;
        margin-top: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 0 15px rgba(0, 255, 213, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# TÍTULO
st.title("⚙️ Quiz: Motor Trifásico de 6 Fios")
st.markdown("### 🧠 Tema: **Conexões Estrela e Triângulo em Motores Trifásicos de 6 Pontas**")
st.markdown("---")
st.write("Responda com **Sim** ou **Não** às perguntas abaixo.")

# PERGUNTAS
perguntas = [
    ("Em uma ligação estrela, os enrolamentos recebem menor tensão que a rede?", True,
    "Sim. Em estrela, a tensão nos enrolamentos é menor que a tensão de linha da rede."),
    ("Em uma ligação triângulo, a tensão de fase é diferente da tensão de linha?", False,
    "Não. Em triângulo, a tensão de fase é igual à tensão de linha."),
    ("Um motor 220/380 V pode ser ligado em triângulo numa rede de 380 V?", False,
    "Não. O motor deve ser ligado em estrela em 380 V. Em triângulo, ele queimaria."),
    ("Ligar um motor projetado para 220 V em 380 V em triângulo pode queimá-lo?", True,
    "Sim. A tensão excede a especificada e pode danificar os enrolamentos."),
    ("A ligação estrela é usada para redes com tensões mais altas?", True,
    "Sim. A ligação estrela reduz a tensão aplicada aos enrolamentos."),
    ("Motores com 6 pontas podem ser ligados em estrela ou triângulo dependendo da rede?", True,
    "Sim. A ligação é escolhida conforme a tensão da rede em relação à tensão nominal do motor."),
    ("A tensão de linha em uma ligação triângulo é menor que a de fase?", False,
    "Não. Em triângulo, a tensão de linha é igual à tensão de fase."),
    ("Ligação estrela reduz a corrente de partida de um motor?", True,
    "Sim. Por aplicar menor tensão, a corrente de partida também é reduzida."),
    ("Motores ligados em triângulo consomem menos corrente que em estrela?", False,
    "Não. Em triângulo, os motores consomem mais corrente, pois recebem maior tensão."),
    ("Um motor de 380 V pode ser ligado em estrela em uma rede de 660 V?", True,
    "Sim. A tensão de linha de 660 V resulta em cerca de 380 V nos enrolamentos em estrela.")
]

# ESTADOS INICIAIS
if "indice" not in st.session_state:
    st.session_state.indice = 0
if "pontuacao" not in st.session_state:
    st.session_state.pontuacao = 0
if "resposta_usuario" not in st.session_state:
    st.session_state.resposta_usuario = None
if "mostrar_resultado" not in st.session_state:
    st.session_state.mostrar_resultado = False
if "pontuou" not in st.session_state:
    st.session_state.pontuou = False
if "historico_pontuacao" not in st.session_state:
    st.session_state.historico_pontuacao = []



def is_process_running(script_name):
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['cmdline'] and script_name in proc.info['cmdline']:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False

# EXECUÇÃO DO QUIZ
if st.session_state.indice < len(perguntas):
    pergunta, resposta_correta, explicacao = perguntas[st.session_state.indice]

    st.subheader(f"❓ Pergunta {st.session_state.indice + 1} de {len(perguntas)}")
    st.markdown(f"<div class='pergunta-caixa'>{pergunta}</div>", unsafe_allow_html=True)

    if not st.session_state.mostrar_resultado:
        col1, col2 = st.columns(2)
        if col1.button("✅ Sim"):
            st.session_state.resposta_usuario = True
            st.session_state.mostrar_resultado = True
            st.rerun()
        if col2.button("❌ Não"):
            st.session_state.resposta_usuario = False
            st.session_state.mostrar_resultado = True
            st.rerun()
    else:
        acertou = (st.session_state.resposta_usuario == resposta_correta)
        if acertou:
            if not st.session_state.pontuou:
                st.session_state.pontuacao += 1
                st.session_state.pontuou = True
            st.success("✔️ Resposta correta!")
        else:
            st.error("❌ Resposta incorreta!")

        with st.expander("🔍 Ver explicação"):
            st.markdown(f"<div class='pergunta-caixa'>{explicacao}</div>", unsafe_allow_html=True)

        if st.button("👉 Próxima pergunta"):
            st.session_state.indice += 1
            st.session_state.resposta_usuario = None
            st.session_state.mostrar_resultado = False
            st.session_state.pontuou = False
            st.rerun()




    


else:
    # FINAL DO QUIZ
    pontuacao_final = st.session_state.pontuacao * 10
    st.balloons()
    st.success(f"🎉 Quiz finalizado! Sua pontuação: {pontuacao_final} de 100")

    if len(st.session_state.historico_pontuacao) == 0 or st.session_state.historico_pontuacao[-1] != pontuacao_final:
        st.session_state.historico_pontuacao.append(pontuacao_final)

    st.subheader("📊 Histórico de Pontuações")
    for i, p in enumerate(st.session_state.historico_pontuacao, 1):
        st.write(f"{i}. {p} pontos")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔁 Recomeçar"):
            st.session_state.indice = 0
            st.session_state.pontuacao = 0
            st.session_state.resposta_usuario = None
            st.session_state.mostrar_resultado = False
            st.session_state.pontuou = False
            st.rerun()

    with col2:
        if st.button("🎮 Iniciar o Jogo de Conexão"):
            if not is_process_running("jogo_motor.py"):
                subprocess.Popen(["python", "jogo_motor.py"])
                st.success("Iniciando o jogo em uma nova janela...")
            else:
                st.error("O jogo já está rodando.")

            




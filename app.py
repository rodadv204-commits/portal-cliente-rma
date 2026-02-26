import streamlit as st
import pandas as pd

st.set_page_config(page_title="Portal do Cliente - RMA", layout="wide")

# ==============================
# BASE DE DADOS SIMPLES (SIMULADA)
# ==============================

CLIENTES = {
    "XPTO123": {
        "empresa": "XPTO LTDA",
        "cnpj": "00.000.000/0001-00",
        "tipo": "Sociedade Limitada",
        "servico": "acordo_quotistas",
        "responsavel": "Rodrigo Alexandre"
    }
}

ESCOPO = {
    "acordo_quotistas": "Estruturação completa do acordo entre sócios, incluindo governança, cláusulas estratégicas, regras de saída e sucessão.",
    "compliance_trabalhista": "Diagnóstico e implementação de medidas preventivas para redução de riscos trabalhistas.",
    "lgpd": "Mapeamento de dados, definição de bases legais e adequação documental à legislação de proteção de dados.",
    "due_diligence": "Análise jurídica, societária e fiscal com relatório estratégico conclusivo."
}

TEMPLATES = {
    "acordo_quotistas": [
        {"nome": "Primeira reunião", "peso": 5},
        {"nome": "Contrato enviado", "peso": 5},
        {"nome": "Contrato assinado", "peso": 10},
        {"nome": "Pagamento confirmado", "peso": 10},
        {"nome": "Documentação completa", "peso": 15},
        {"nome": "Minuta preliminar", "peso": 25},
        {"nome": "Reunião de validação", "peso": 10},
        {"nome": "Entrega final", "peso": 20},
    ]
}

DOCUMENTOS_OBRIGATORIOS = {
    "acordo_quotistas": [
        "Contrato Social",
        "Alterações Contratuais",
        "Documento Sócio 1",
        "Documento Sócio 2"
    ]
}

# ==============================
# FUNÇÕES
# ==============================

def inicializar_etapas(servico):
    return [{"nome": e["nome"], "peso": e["peso"], "concluida": False} for e in TEMPLATES[servico]]

def calcular_progresso(etapas):
    return sum(e["peso"] for e in etapas if e["concluida"])

def status_atual(etapas):
    for etapa in etapas:
        if not etapa["concluida"]:
            return etapa["nome"]
    return "Projeto concluído"

# ==============================
# LOGIN
# ==============================

st.sidebar.title("Área do Cliente")
codigo = st.sidebar.text_input("Código de acesso")

if codigo in CLIENTES:

    cliente = CLIENTES[codigo]

    if "etapas" not in st.session_state:
        st.session_state.etapas = inicializar_etapas(cliente["servico"])

    if "documentos" not in st.session_state:
        st.session_state.documentos = {doc: False for doc in DOCUMENTOS_OBRIGATORIOS[cliente["servico"]]}

    if "parcelas" not in st.session_state:
        st.session_state.parcelas = [{"parcela": 1, "paga": False},
                                     {"parcela": 2, "paga": False},
                                     {"parcela": 3, "paga": False}]

    # ==============================
    # CABEÇALHO
    # ==============================

    st.title("Portal do Cliente")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"**Empresa:** {cliente['empresa']}")
        st.markdown(f"**CNPJ:** {cliente['cnpj']}")
        st.markdown(f"**Tipo societário:** {cliente['tipo']}")

    with col2:
        st.markdown(f"**Serviço contratado:** {cliente['servico'].replace('_', ' ').title()}")
        st.markdown(f"**Responsável técnico:** {cliente['responsavel']}")

    st.divider()

    # ==============================
    # ESCOPO
    # ==============================

    st.subheader("Escopo do Serviço")
    st.info(ESCOPO[cliente["servico"]])

    # ==============================
    # DOCUMENTOS
    # ==============================

    st.subheader("Documentação")

    for doc in st.session_state.documentos:
        col1, col2 = st.columns([3,1])
        with col1:
            st.write(doc)
        with col2:
            if not st.session_state.documentos[doc]:
                uploaded = st.file_uploader(f"Enviar {doc}", key=doc)
                if uploaded:
                    st.session_state.documentos[doc] = True
            else:
                st.success("Recebido")

    # Verifica se todos documentos enviados
    if all(st.session_state.documentos.values()):
        for etapa in st.session_state.etapas:
            if etapa["nome"] == "Documentação completa":
                etapa["concluida"] = True

    # ==============================
    # PAGAMENTO
    # ==============================

    st.subheader("Pagamento")

    for p in st.session_state.parcelas:
        p["paga"] = st.checkbox(f"Parcela {p['parcela']} paga", value=p["paga"])

    if all(p["paga"] for p in st.session_state.parcelas):
        for etapa in st.session_state.etapas:
            if etapa["nome"] == "Pagamento confirmado":
                etapa["concluida"] = True

    # ==============================
    # CHECKLIST
    # ==============================

    st.subheader("Etapas do Projeto")

    for etapa in st.session_state.etapas:
        etapa["concluida"] = st.checkbox(
            f"{etapa['nome']} ({etapa['peso']}%)",
            value=etapa["concluida"]
        )

    # ==============================
    # PROGRESSO
    # ==============================

    progresso = calcular_progresso(st.session_state.etapas)

    st.divider()
    st.subheader("Progresso do Projeto")

    st.progress(progresso / 100)
    st.markdown(f"### {progresso}% concluído")
    st.markdown(f"**Etapa atual:** {status_atual(st.session_state.etapas)}")

    # ==============================
    # REUNIÕES
    # ==============================

    st.subheader("Registro de Reuniões")

    if "reunioes" not in st.session_state:
        st.session_state.reunioes = []

    with st.form("nova_reuniao"):
        data = st.date_input("Data da reunião")
        resumo = st.text_area("Resumo da reunião")
        enviar = st.form_submit_button("Salvar")

        if enviar:
            st.session_state.reunioes.append({"data": data, "resumo": resumo})

    for r in st.session_state.reunioes:
        st.markdown(f"**{r['data']}**")
        st.write(r["resumo"])
        st.divider()

else:
    st.warning("Insira seu código de acesso na lateral.")

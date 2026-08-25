import streamlit as st
import uuid

st.set_page_config(
    page_title="Todo List",
    page_icon="✅",
    layout="centered"
)

# ----------------------------
# Style
# ----------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #f5f7ff 0%, #eef6ff 100%);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .card {
        background: rgba(255,255,255,0.85);
        backdrop-filter: blur(10px);
        border-radius: 22px;
        padding: 1.2rem 1.1rem;
        box-shadow: 0 12px 30px rgba(31, 41, 55, 0.08);
        border: 1px solid rgba(148, 163, 184, 0.15);
    }

    .title {
        font-size: 2.3rem;
        font-weight: 800;
        color: #111827;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        color: #6b7280;
        font-size: 1rem;
    }

    div[data-testid="stTextInput"] > div > div > input {
        border-radius: 14px;
        border: 1px solid #dbe3f0;
        padding: 0.85rem 1rem;
        font-size: 1rem;
        background: white;
    }

    div[data-testid="stButton"] > button {
        border-radius: 14px;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        border: none;
        font-weight: 700;
        padding: 0.75rem 1.1rem;
        transition: 0.2s ease;
    }

    div[data-testid="stButton"] > button:hover {
        opacity: 0.95;
        transform: translateY(-1px);
    }

    [data-testid="stCheckbox"] {
        margin-top: 0.2rem;
    }

    .done-text {
        color: #9ca3af;
        text-decoration: line-through;
    }

    .task-row {
        background: #f8fafc;
        border-radius: 14px;
        padding: 0.7rem 0.8rem;
        margin: 0.5rem 0;
        border: 1px solid #e5e7eb;
    }

    .stat-box {
        background: white;
        border-radius: 16px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 8px 18px rgba(15, 23, 42, 0.05);
        border: 1px solid #edf2f7;
    }

    .stat-number {
        font-size: 1.8rem;
        font-weight: 800;
        color: #111827;
    }

    .stat-label {
        color: #64748b;
        font-size: 0.8rem;
        margin-top: 0.2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# State
# ----------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {"id": str(uuid.uuid4()), "text": "Préparer le plan du projet", "done": False},
        {"id": str(uuid.uuid4()), "text": "Réviser la présentation", "done": True},
        {"id": str(uuid.uuid4()), "text": "Répondre aux emails", "done": False},
    ]

# ----------------------------
# Helpers
# ----------------------------
def add_task(task_text):
    if task_text.strip():
        st.session_state.tasks.append({
            "id": str(uuid.uuid4()),
            "text": task_text.strip(),
            "done": False
        })

def delete_task(task_id):
    st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != task_id]

def toggle_task(task_id):
    for task in st.session_state.tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]
            break

# ----------------------------
# Page UI
# ----------------------------
st.markdown('<div class="title">✅ Todo List</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Ajoute ce que tu dois faire et coche quand c’est terminé.</div>', unsafe_allow_html=True)

# Stats
total_tasks = len(st.session_state.tasks)
done_tasks = sum(1 for t in st.session_state.tasks if t["done"])
pending_tasks = total_tasks - done_tasks

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'''
        <div class="stat-box">
            <div class="stat-number">{total_tasks}</div>
            <div class="stat-label">Total</div>
        </div>
    ''', unsafe_allow_html=True)
with col2:
    st.markdown(f'''
        <div class="stat-box">
            <div class="stat-number">{done_tasks}</div>
            <div class="stat-label">Faites</div>
        </div>
    ''', unsafe_allow_html=True)
with col3:
    st.markdown(f'''
        <div class="stat-box">
            <div class="stat-number">{pending_tasks}</div>
            <div class="stat-label">À faire</div>
        </div>
    ''', unsafe_allow_html=True)

st.write("")

# Add task
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    col_input, col_button = st.columns([5, 1])
    with col_input:
        new_task = st.text_input(
            "Ajouter une tâche",
            placeholder="Ex: Finaliser le rapport...",
            label_visibility="collapsed"
        )
    with col_button:
        st.write("")
        if st.button("Ajouter", use_container_width=True):
            add_task(new_task)

    st.markdown('</div>', unsafe_allow_html=True)

st.write("")

# Display tasks
for task in st.session_state.tasks:
    col_check, col_text, col_delete = st.columns([0.7, 5.2, 0.8])

    with col_check:
        checked = st.checkbox(" ", key=f"check_{task['id']}", value=task["done"])
        if checked != task["done"]:
            toggle_task(task["id"])

    with col_text:
        if task["done"]:
            st.markdown(f'<div class="task-row"><span class="done-text">{task["text"]}</span></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="task-row">{task["text"]}</div>', unsafe_allow_html=True)

    with col_delete:
        if st.button("❌", key=f"delete_{task['id']}", use_container_width=True):
            delete_task(task["id"])
            st.rerun()

st.write("")
st.caption("💡 Astuce : coche une tâche pour la marquer comme terminée.")

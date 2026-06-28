import streamlit as st
from migration_engine import apply_migration

st.set_page_config(
    page_title="AI Code Migration Assistant",
    page_icon="🚀",
    layout="wide"
)

# ============================================================
# CUSTOM CSS (Dark Theme)
# ============================================================

st.markdown("""
<style>
    .stApp { background: #0f1117; }
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00d4ff 0%, #7b2ff7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0 0.5rem 0;
    }
    .sub-header {
        text-align: center;
        font-size: 1.1rem;
        color: #888;
        margin-bottom: 2rem;
    }
    .stButton button {
        background: linear-gradient(135deg, #00d4ff 0%, #7b2ff7 100%);
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        border: none;
        transition: 0.3s ease;
        width: 100%;
    }
    .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 14px rgba(0, 212, 255, 0.3);
    }
    .stTextArea textarea, .stTextInput input {
        background: #1e1e2e !important;
        color: #cdd6f4 !important;
        border: 1px solid #2a2a3e !important;
        border-radius: 8px !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 0 2px rgba(0, 212, 255, 0.2) !important;
    }
    .footer {
        text-align: center;
        color: #444;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding: 1.5rem 0 0.5rem 0;
        border-top: 1px solid #1e1e2e;
    }
    .footer a { color: #00d4ff; text-decoration: none; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

st.markdown('<div class="main-header">🚀 AI Code Migration Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Bulk rename variables and arguments using AST transformation</div>', unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/python.png", width=80)
    st.markdown("---")
    st.markdown("### ⚙️ How It Works")
    st.markdown("""
    1. **Paste** your Python code  
    2. **Add** rename mappings (old → new)  
    3. **Migrate** — AST transforms the code  
    """)
    st.markdown("---")
    st.markdown("### 🔐 Security")
    st.markdown("✅ Your code is **not stored**")

# ============================================================
# MAIN UI
# ============================================================

col_left, col_right = st.columns([3, 1])

with col_left:
    code_input = st.text_area(
        "📄 Paste your Python code here:",
        height=300,
        value='''def add(a, b):
    return a + b

def greet(name):
    print(f"Hello, {name}")''',
        help="Paste your Python code and click 'Migrate' to transform it."
    )

with col_right:
    st.markdown("### 🔄 Rename Mapping")
    
    # Initialize session state for mappings
    if "mappings" not in st.session_state:
        st.session_state.mappings = [{"old": "a", "new": "x"}]
    
    # Display mapping rows
    for i, mapping in enumerate(st.session_state.mappings):
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            mapping["old"] = st.text_input("Old", mapping["old"], key=f"old_{i}")
        with col2:
            mapping["new"] = st.text_input("New", mapping["new"], key=f"new_{i}")
        with col3:
            if st.button("❌", key=f"del_{i}"):
                st.session_state.mappings.pop(i)
                st.rerun()
    
    # Add mapping button
    if st.button("➕ Add Mapping", use_container_width=True):
        st.session_state.mappings.append({"old": "", "new": ""})
        st.rerun()
    
    st.markdown("---")
    migrate_btn = st.button("🚀 Migrate Code", use_container_width=True)

# ============================================================
# MIGRATION LOGIC
# ============================================================

if migrate_btn:
    if not code_input.strip():
        st.warning("⚠️ Please paste some code to migrate.")
    else:
        # Build rename map from session state
        rename_map = {}
        for mapping in st.session_state.mappings:
            if mapping["old"].strip() and mapping["new"].strip():
                rename_map[mapping["old"].strip()] = mapping["new"].strip()
        
        if not rename_map:
            st.warning("⚠️ Please add at least one valid rename mapping.")
        else:
            with st.spinner("🔄 Applying AST transformation..."):
                migrated_code = apply_migration(code_input, rename_map)
            
            if "❌" in migrated_code:
                st.error(migrated_code)
            else:
                st.markdown("---")
                st.subheader("📊 Migration Result")
                
                col_before, col_after = st.columns(2)
                with col_before:
                    st.markdown("**❌ Before**")
                    st.code(code_input, language="python")
                with col_after:
                    st.markdown("**✅ After**")
                    st.code(migrated_code, language="python")

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    Built with ❤️ using Streamlit • AST<br>
    <a href="https://github.com/Rohits533/AI-Code-Migration-Assistant" target="_blank">View on GitHub</a>
</div>
""", unsafe_allow_html=True)

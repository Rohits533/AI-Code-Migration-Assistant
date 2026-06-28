
---

## 📄 `app.py` (Complete & Correct — with AI Integration)

```python
import streamlit as st
from migration_engine import apply_migration
from ai_review import review_migration

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
st.markdown('<div class="sub-header">Automatically rename variables and arguments using AST transformation + AI explanations</div>', unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/python.png", width=80)
    st.markdown("---")
    st.markdown("### ⚙️ How It Works")
    st.markdown("""
    1. **Paste** your Python code  
    2. **Define** rename mappings (old → new)  
    3. **Migrate** — AST transforms the code  
    4. **Review** — AI explains what changed
    """)
    st.markdown("---")
    st.markdown("### 🔐 Security")
    st.markdown("✅ Your code is **not stored**")
    st.markdown("✅ API key is securely stored in Streamlit Secrets")
    st.markdown("---")
    st.markdown("### 📊 Stats")
    st.markdown(f"**Migrations:** 0 (pending)")

# ============================================================
# GET API KEY FROM SECRETS
# ============================================================

try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("🚨 GROQ_API_KEY not found in Streamlit Secrets. Please add it in the app settings.")
    groq_api_key = None

# ============================================================
# MAIN UI
# ============================================================

col_left, col_right = st.columns([3, 1])

with col_left:
    code_input = st.text_area(
        "📄 Paste your Python code here:",
        height=300,
        value='''def add(a, b):
    return a + b''',
        help="Paste your Python code and click 'Migrate' to transform it."
    )

with col_right:
    st.markdown("### 🔄 Rename Mapping")
    old_name = st.text_input("Old name", "a")
    new_name = st.text_input("New name", "x")
    st.markdown("---")
    st.markdown("### ⚡ Quick Actions")
    migrate_btn = st.button("🚀 Migrate Code", use_container_width=True)

# ============================================================
# MIGRATION LOGIC
# ============================================================

if migrate_btn:
    if not code_input.strip():
        st.warning("⚠️ Please paste some code to migrate.")
    elif not old_name.strip() or not new_name.strip():
        st.warning("⚠️ Please enter both old and new names.")
    else:
        with st.spinner("🔄 Applying AST transformation..."):
            rename_map = {old_name: new_name}
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
            
            # AI Review (only if API key exists)
            if groq_api_key:
                try:
                    with st.spinner("🧠 Getting AI summary..."):
                        ai_summary = review_migration(code_input, migrated_code, groq_api_key)
                    
                    st.markdown("---")
                    st.subheader("🧠 AI Summary")
                    st.info(ai_summary)
                except Exception as e:
                    st.warning(f"⚠️ AI review failed: {e}")
            else:
                st.info("ℹ️ AI review is disabled. Add a GROQ_API_KEY to enable it.")

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    Built with ❤️ using Streamlit • AST • Groq API<br>
    <a href="https://github.com/Rohits533/AI-Code-Migration-Assistant" target="_blank">View on GitHub</a>
</div>
""", unsafe_allow_html=True)

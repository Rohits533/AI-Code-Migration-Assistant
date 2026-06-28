import streamlit as st
from migration_engine import apply_migration

st.set_page_config(page_title="AI Code Migration Assistant", layout="wide")

st.title("🤖 AI Code Migration Assistant")
st.markdown("Rename variables and function arguments using AST transformation.")

# Input
code_input = st.text_area(
    "📄 Paste your Python code:",
    height=250,
    value='''def add(a, b):
    return a + b
'''
)

st.markdown("### 🔄 Rename Mapping")
col1, col2 = st.columns(2)
old_name = col1.text_input("Old name", "a")
new_name = col2.text_input("New name", "x")

if st.button("🚀 Migrate Code"):
    if old_name and new_name:
        rename_map = {old_name: new_name}
        result = apply_migration(code_input, rename_map)
        
        st.markdown("---")
        st.subheader("✅ Migrated Code")
        st.code(result, language="python")
    else:
        st.warning("Please enter both old and new names.")

# app.py
import streamlit as st
import requests
import os
from io import BytesIO
from datetime import datetime

# Try to import reportlab for PDF export; if not available, fallback to simple txt download.
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    REPORTLAB_AVAILABLE = True
except Exception:
    REPORTLAB_AVAILABLE = False

# Page config
st.set_page_config(page_title="Akuntan Pintar AI", page_icon="📘", layout="centered")

# -------------------------
# --- Styling & Themes ---
# -------------------------
# Default theme = light. We'll inject CSS according to toggle.
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

def set_dark_mode(value: bool):
    st.session_state.dark_mode = value

# Inject CSS for light & dark
light_css = """
:root{
  --bg:#ffffff;
  --card:#F7F9FC;
  --text:#0b1726;
  --muted:#4a5568;
  --accent:#1E88E5;
}
body { background-color: var(--bg); color: var(--text); }
.stButton>button { background-color: var(--accent); color: white; border-radius:8px; padding:8px 12px; }
"""
dark_css = """
:root{
  --bg:#0f1720;           /* dark background */
  --card:#0b1220;         /* card bg */
  --text:#E6EEF8;         /* near white text */
  --muted:#9FB0C8;        /* muted text */
  --accent:#1E88E5;       /* blue accent */
}
body { background-color: var(--bg); color: var(--text); }
.stButton>button { background-color: var(--accent); color: white; border-radius:8px; padding:8px 12px; }
"""

# Shared CSS for layout
shared_css = """
<style>
/* Center header */
.header { text-align: center; margin-bottom: 6px; }
.subtitle { text-align: center; color: var(--muted); margin-bottom: 18px; }
/* TextArea height */
.stTextArea textarea { height: 120px !important; }
/* Result card */
.result-card {
  background-color: var(--card);
  border: 1px solid rgba(255,255

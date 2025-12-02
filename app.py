import streamlit as st
import requests
import os

# Page config
st.set_page_config(page_title="Akuntan Pintar AI", page_icon="📘", layout="centered")

# Custom CSS for better UI
st.markdown("""
    <style>
        .title {
            text-align: center;
            font-size: 40px;
            font-weight: 700;
            color: #0D47A1;
        }
        .subtitle {
            text-align: center;
            font-size: 18px;
            color: #555;
            margin-bottom: 25px;
        }
        .stTextArea textarea {
            height: 120px !important;
        }
        .result-box {
            background-color: #F7F9FC;
            border: 1px solid #d0d7de;
            padding: 18px;
            border-radius: 10px;
            margin-top: 15px;
        }
        .run-btn button {
            width: 100%;
            border-radius: 8px;
            font-weight: 600;
            font-size: 18px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="title">📘 Akuntan Pintar AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Asisten Akuntansi Cerdas berbasis AI</div>', unsafe_allow_html=True)

# Input prompt
prompt = st.text_area(
    "Masukkan perintah atau pertanyaan akuntansi:",
    placeholder="Contoh: Buat jurnal untuk pembelian persediaan Rp 5.000.000 secara kredit"
)

api_key = os.getenv("GROQ_API_KEY")

# Button to run AI
if st.button("Jalankan AI", key="run_btn"):
    if not prompt:
        st.warning("Masukkan prompt terlebih dahulu.")
    else:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        data = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "You are an accounting assistant."},
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data
        )

        result = response.json()

        # Display result in styled box
        st.markdown("### Hasil:")
        st.markdown(f"<div class='result-box'>{result['choices'][0]['message']['content']}</div>", unsafe_allow_html=True)

import streamlit as st
import requests
import os

st.set_page_config(page_title="Akuntan Pintar AI", page_icon="📘")

st.title("📘 Akuntan Pintar AI")
st.write("Aplikasi Akuntansi cerdas berbasis Streamlit + Groq API.")

# Ambil API Key dari Streamlit Secrets
api_key = os.getenv("GROQ_API_KEY")

prompt = st.text_area("Masukkan perintah atau pertanyaan akuntansi:")

if st.button("Jalankan AI"):
    if not prompt:
        st.warning("Masukkan prompt.")
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
        st.write("### Hasil:")
        st.write(result["choices"][0]["message"]["content"])

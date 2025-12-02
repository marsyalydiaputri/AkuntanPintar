import streamlit as st
import requests
import base64

st.set_page_config(page_title="Akuntan Pintar AI", page_icon="📘")

st.title("📘 Akuntan Pintar AI")
st.write("Aplikasi Akuntansi cerdas berbasis Streamlit + Groq API.")

# Input API Key (dari Groq)
api_key = st.text_input("Masukkan Groq API Key kamu:", type="password")

# Input perintah
prompt = st.text_area("Masukkan perintah atau pertanyaan akuntansi:")

if st.button("Jalankan AI"):
    if not api_key:
        st.warning("Masukkan API key terlebih dahulu.")
    elif not prompt:
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

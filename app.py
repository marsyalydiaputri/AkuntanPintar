import streamlit as st
import requests
import os

st.set_page_config(page_title="Akuntan Pintar AI", page_icon="📘")

st.title("📘 Akuntan Pintar AI")
st.write("Asisten Akuntansi Cerdas berbasis AI")

# Ambil API Key dari environment (Streamlit Cloud Secrets)
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("API Key tidak ditemukan! Pastikan sudah diatur di Secrets.")
    st.stop()

prompt = st.text_area(
    "Masukkan perintah atau pertanyaan akuntansi:",
    placeholder="Contoh: Buat jurnal pembelian persediaan Rp 50.000.000 secara kredit"
)

if st.button("Jalankan AI"):
    if not prompt:
        st.warning("Masukkan prompt terlebih dahulu.")
    else:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        data = {
    "model": "llama3-70b-8192",
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

        try:
            result = response.json()

            if "choices" in result:
                st.success("Berhasil!")
                st.write("### Hasil:")
                st.write(result["choices"][0]["message"]["content"])
            else:
                st.error("Terjadi kesalahan API!")
                st.code(result)

        except Exception as e:
            st.error("Error memproses response!")
            st.write(str(e))

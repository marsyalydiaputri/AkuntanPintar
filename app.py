# Inisialisasi Groq Client
client = Groq(api_key=GROQ_API_KEY)

# Judul Aplikasi
st.title("📘 Akuntan Pintar AI")
st.write("Sistem Akuntansi Cerdas berbasis Foto, Suara, dan Teks")


# ============================
# 1. FOTO → OCR → JURNAL
# ============================
st.header("📸 Input Struk / Foto Transaksi")

uploaded_image = st.file_uploader("Upload Foto Struk (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Foto Terunggah", use_column_width=True)

    # OCR via Groq Vision API
    if st.button("Proses OCR & Buat Jurnal"):
        img_bytes = uploaded_image.read()

        result = client.chat.completions.create(
            model="llama-3.2-90b-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": "Extract text & create accounting journal entry"},
                        {"type": "input_image", "image_url": "data:image/jpeg;base64," + img_bytes.hex()}
                    ],
                }
            ]
        )

        ocr_output = result.choices[0].message.content
        st.success("Berhasil diproses!")
        st.write(ocr_output)


# ============================
# 2. SUARA → STT → JURNAL
# ============================
st.header("🎤 Input Suara (Speech-to-Text)")

uploaded_audio = st.file_uploader("Upload Audio (.mp3 / .wav)", type=["mp3", "wav"])

if uploaded_audio:
    if st.button("Konversi Suara & Buat Jurnal"):
        audio_bytes = uploaded_audio.read()

        response = client.audio.transcriptions.create(
            file=("voice.mp3", audio_bytes),
            model="whisper-large-v3",
            response_format="text"
        )

        st.write("Teks Hasil Speech-to-Text:")
        st.info(response)

        # Generate jurnal dari teks
        journal = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[{"role": "user", "content": f"Buatkan jurnal dari transaksi berikut: {response}"}]
        )

        st.write("Jurnal Otomatis:")
        st.success(journal.choices[0].message.content)


# ============================
# 3. CHAT → JURNAL
# ============================
st.header("💬 Input Teks Manual")

text_input = st.text_area("Masukkan deskripsi transaksi")

if st.button("Buat Jurnal"):
    result = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[{"role": "user", "content": f"Buatkan jurnal untuk transaksi: {text_input}"}]
    )
    st.success(result.choices[0].message.content)


# ============================
# 4. Fraud Detection
# ============================
st.header("⚠️ Deteksi Fraud / Anomali")

fraud_data = st.text_area("Masukkan daftar transaksi (boleh acak)")

if st.button("Cek Fraud"):
    fd = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[{"role": "user", "content": f"Analisis fraud pada transaksi berikut:\n{fraud_data}"}]
    )
    st.warning(fd.choices[0].message.content)


# ============================
# 5. Prediksi Arus Kas
# ============================
st.header("📈 Prediksi Arus Kas Sederhana")

cashflow_input = st.text_area("Masukkan histori cash flow (angka per baris)")

if st.button("Prediksi"):
    pred = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[{"role": "user", "content": f"Buat prediksi arus kas dari data ini:\n{cashflow_input}"}]
    )
    st.info(pred.choices[0].message.content)

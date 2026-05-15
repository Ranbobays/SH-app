import os
import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import io

# 1. Setting Tampilan (Agar lebih lebar dan nyaman)
st.set_page_config(page_title="Future Vision AI", page_icon="⚖️", layout="wide")

# Custom CSS untuk memperbesar area ketik
st.markdown("""
    <style>
    .stTextArea textarea { font-size: 1.1rem !important; }
    .main { background-color: #0f172a; }
    </style>
    """, unsafe_allow_html=True)

def generate():
    # --- KONEKSI API ---
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        st.error("API Key belum terpasang di Secrets!")
        return
    client = genai.Client(api_key=api_key)

    # --- HEADER ---
    st.title("⚖️ Future Vision: Multi-Modal Contract Simulator")
    st.write("Analisis kontrak melalui teks, dokumen PDF, atau foto hasil jepretan.")

    # --- INPUT AREA ---
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📝 Input Kontrak")
        # Tempat ketikan yang lebih besar
        user_input = st.text_area(
            "Ketikan teks kontrak atau tambahan instruksi:",
            height=400,
            placeholder="Tempel teks di sini atau beri instruksi tambahan untuk file yang diunggah..."
        )

    with col2:
        st.subheader("📁 Unggah Lampiran")
        uploaded_file = st.file_uploader("Pilih PDF atau Foto Kontrak", type=['pdf', 'jpg', 'jpeg', 'png'])
        
        if uploaded_file is not None:
            if uploaded_file.type == "application/pdf":
                st.success("PDF berhasil dimuat!")
            else:
                image = Image.open(uploaded_file)
                st.image(image, caption="Preview Foto", use_container_width=True)

    # --- TOMBOL ANALISIS ---
    if st.button("🚀 Mulai Analisis Mendalam", use_container_width=True):
        if user_input or uploaded_file:
            with st.spinner("🧠 Sedang berpikir mendalam (Thinking Mode)..."):
                try:
                    # Menyiapkan part isi pesan
                    prompt_parts = []
                    
                    # Jika ada teks
                    if user_input:
                        prompt_parts.append(types.Part.from_text(text=user_input))
                    
                    # Jika ada file (PDF atau Foto)
                    if uploaded_file:
                        file_bytes = uploaded_file.read()
                        mime_type = uploaded_file.type
                        prompt_parts.append(types.Part.from_bytes(data=file_bytes, mime_type=mime_type))

                    # --- INI "OTAK" ASLI KAMU (TIDAK DIUBAH) ---
                    model = "gemini-2.0-flash-thinking-exp" # Gunakan versi thinking terbaru
                    
                    generate_content_config = types.GenerateContentConfig(
                        thinking_config=types.ThinkingConfig(
                            thinking_level="HIGH",
                        ),
                        tools=[types.Tool(google_search=types.GoogleSearch())],
                    )

                    # Memanggil AI
                    response = client.models.generate_content(
                        model=model,
                        contents=[types.Content(role="user", parts=prompt_parts)],
                        config=generate_content_config,
                    )
                    
                    # --- MENAMPILKAN HASIL ---
                    st.markdown("---")
                    st.subheader("🔍 Hasil Analisis Future Vision")
                    st.markdown(response.text)
                    
                    # Tombol Ekspor
                    st.download_button(
                        label="📥 Ekspor Analisis ke Teks",
                        data=response.text,
                        file_name="analisis_kontrak.txt",
                        mime="text/plain"
                    )

                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")
        else:
            st.warning("Masukkan teks atau unggah file terlebih dahulu!")

if __name__ == "__main__":
    generate()

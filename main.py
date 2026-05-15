import os
import streamlit as st
from google import genai
from google.genai import types

# 1. Konfigurasi Halaman (Biar tampilan Web Bagus)
st.set_page_config(page_title="Future Vision AI", page_icon="⚖️")

def generate():
    # MENGAMBIL API KEY (Pastikan sudah diisi di Secrets Streamlit Cloud)
    # Jika run di laptop, ganti dengan "AIza..." langsung
    api_key = os.environ.get("GEMINI_API_KEY") 
    
    if not api_key:
        st.error("API Key belum terpasang di Secrets!")
        return

    client = genai.Client(api_key=api_key)

    # UI INPUT UNTUK USER
    st.title("⚖️ Future Vision: Contract Simulator")
    user_input = st.text_area("Masukkan teks kontrak:", placeholder="Ketik di sini...")
    
    if st.button("Analisis Kontrak 🚀"):
        if user_input:
            # BAGIAN OTAK AI STUDIO (JANGAN DIUBAH)
            model = "gemini-3-flash-preview"
            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=user_input), # Mengambil input dari box
                    ],
                ),
            ]
            
            # Tambahkan System Instruction kamu di sini jika ada!
            generate_content_config = types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(
                    thinking_level="HIGH",
                ),
                tools=[types.Tool(googleSearch=types.GoogleSearch())],
            )

            # MENAMPILKAN HASIL KE LAYAR STREAMLIT
            with st.spinner("Sedang berpikir mendalam..."):
                try:
                    # Ganti generate_content_stream menjadi generate_content biasa agar lebih mudah tampil di web
                    response = client.models.generate_content(
                        model=model,
                        contents=contents,
                        config=generate_content_config,
                    )
                    
                    st.markdown("### Hasil Analisis")
                    st.write(response.text)
                    
                    # Fitur Download (PDF simpel dalam bentuk teks)
                    st.download_button(
                        label="Ekspor Hasil ke TXT",
                        data=response.text,
                        file_name="hasil_kontrak.txt",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat memanggil AI: {e}")
        else:
            st.warning("Isi dulu kontraknya bos!")

if __name__ == "__main__":
    generate()

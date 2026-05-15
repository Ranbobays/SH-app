import streamlit as st
from google import genai
from google.genai import types
import os

# Konfigurasi Tampilan Web
st.set_page_config(
    page_title="Future Vision - Simulator Kontrak",
    page_icon="⚖️",
    layout="centered"
)

# Judul dan Deskripsi
st.title("⚖️ Future Vision: Simulator Kontrak")
st.subheader("Cek masa depanmu sebelum tanda tangan!")
st.write("Aplikasi ini menganalisis kontrak kerja menggunakan AI berdasarkan UU Ketenagakerjaan Indonesia.")

# Sidebar untuk Pengaturan
with st.sidebar:
    st.header("Konfigurasi")
    api_key = st.text_input("Masukkan Gemini API Key:", type="password")
    st.info("Dapatkan API Key gratis di [Google AI Studio](https://aistudio.google.com/)")
    st.markdown("---")
    st.write("Dibuat untuk #JuaraVibeCoding")

# Area Input Kontrak
kontrak_input = st.text_area(
    "Tempel Teks Kontrak atau Pasal di sini:",
    height=300,
    placeholder="Contoh: Pasal 5 tentang gaji dan lembur..."
)

# Tombol Analisis
if st.button("Simulasikan Masa Depan 🚀"):
    if not api_key:
        st.error("Silakan masukkan API Key di sebelah kiri dulu ya!")
    elif not kontrak_input:
        st.warning("Teks kontraknya masih kosong, nih.")
    else:
        try:
            # Hubungkan ke Gemini
            client = genai.Client(api_key=api_key)
            
            # Instruksi Sistem (Otak si AI)
            sys_instr = (
                "Anda adalah pakar hukum ketenagakerjaan Indonesia. "
                "Tugas Anda adalah menganalisis kontrak dan memberikan simulasi masa depan. "
                "1. SUMMARY: Jelaskan isi kontrak dengan bahasa santai. "
                "2. LEGAL CHECK: Bandingkan dengan UU No. 13/2003 dan UU Cipta Kerja. "
                "3. FUTURE SCENARIO: Ceritakan apa yang terjadi jika pengguna resign atau kena PHK. "
                "4. RED FLAGS: Berikan poin peringatan jika ada pasal yang merugikan. "
                "Gunakan bahasa yang mudah dimengerti tapi tetap tegas."
            )

            with st.spinner('Sedang menghitung masa depan...'):
                response = client.models.generate_content(
                    model="gemini-2.0-flash-exp",
                    contents=kontrak_input,
                    config=types.GenerateContentConfig(system_instruction=sys_instr)
                )
                
                # Menampilkan Hasil
                st.success("Analisis Selesai!")
                st.markdown("---")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Waduh, ada error: {str(e)}")

# Footer
st.markdown("---")
st.caption("Catatan: Hasil analisis AI ini adalah simulasi dan bukan saran hukum resmi.")
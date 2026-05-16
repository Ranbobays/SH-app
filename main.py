import streamlit as st
from groq import Groq

client = Groq(
    api_key=st.secrets["GROK_API_KEY"]
)

prompt = """
Analisa kontrak kerja berikut.

Fokus:
- klausul ambigu
- potensi eksploitasi
- overtime abuse
- privacy overreach
- asymmetrical obligation

Berikan:
1. Ringkasan
2. Red flags
3. Severity score 1-10

Kontrak:
Karyawan wajib fleksibel terhadap kebutuhan operasional perusahaan dan bersedia dihubungi di luar jam kerja.
"""

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    model="llama-3.1-8b-instant"
)

print(chat_completion.choices[0].message.content)
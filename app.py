import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Shipra: MP3 Converter", page_icon="🎵")

st.title("🎵 Shipra: Universal MP3 Converter")
st.write("सभ्य और सुरक्षित तरीके से किसी भी लिंक को ऑडियो में बदलें।")

url = st.text_input("यहाँ वीडियो का लिंक डालें:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("MP3 तैयार करें"):
    if url:
        try:
            with st.spinner('Shipra आपके लिए फाइल तैयार कर रही है...'):
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': 'shipra_audio.%(ext)s',
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                with open("shipra_audio.mp3", "rb") as f:
                    st.audio(f.read(), format="audio/mp3")
                    st.download_button("MP3 डाउनलोड करें", f, "shipra_music.mp3")
                os.remove("shipra_audio.mp3")
        except Exception as e:
            st.error("त्रुटि: यह लिंक अभी काम नहीं कर रहा। कृपया दूसरा लिंक आज़माएँ।")
    else:
        st.warning("कृपया पहले लिंक डालें।")
        

import streamlit as st
import requests
from tools.logo import LogoAiTool

st.set_page_config(page_title="Logo Generator", page_icon="🎨")

logo_ai = LogoAiTool()

st.title("Logo Generator")
logo_style = st.sidebar.selectbox("The style of your logo", ("lettermark", "mascot", "pictorial","emblem"))
subject = st.sidebar.text_input("The subject of your logo")
add_req = st.sidebar.text_input("Any additional requirements")
theme_color = st.sidebar.color_picker("Your logo's theme color")
generate = st.sidebar.button("Generate", disabled=not bool(subject))
if generate:
    with st.spinner("Generating Logo..."):
        image_url = logo_ai.generate_image(logo_style=logo_style, subject=subject, add_req=add_req, theme_color=theme_color)
    st.image(image_url, width=400)
    response = requests.get(image_url, stream=True)
    st.download_button(
            label="Download Image",
            data=response.content,
            file_name=f"{logo_style}.png",
            mime="image/png"
          )


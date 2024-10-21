import streamlit as st
import requests
from tools.image import ImageAiTool
from datetime import datetime

st.set_page_config(page_title="Image Generator", page_icon="🏞️")

image_ai = ImageAiTool()

st.title("Image Generator")

prompt = st.sidebar.text_input("Image prompt...")
quality = st.sidebar.selectbox("Quality of the image", ("standard", "hd"))

generate = st.sidebar.button("Generate", disabled=not bool(prompt))
current_datetime_iso = datetime.now().replace(microsecond=0).isoformat()
if generate:
    with st.spinner("Generating Image..."):
        image_url = image_ai.generate_image(prompt=prompt, quality=quality)
    st.image(image_url, width=400)
    response = requests.get(image_url, stream=True)
    st.download_button(
            label="Download Image",
            data=response.content,
            file_name=f"generated_{current_datetime_iso}.png",
            mime="image/png"
          )


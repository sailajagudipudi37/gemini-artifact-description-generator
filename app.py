
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()

# Configure API key
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)
def get_gemini_response(input_text, prompt):
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    response = model.generate_content(input_text + "\n" + prompt)
    return response.text




# Milestone 3: Function for Image Setup
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
# Page Configuration & Header
st.set_page_config(page_title="Gemini Historical Artifact Description")

st.header("🏛 Gemini Historical Artifact Description App")
# Step 5.2: User Inputs
input_text = st.text_input("Input Prompt:", key="input")

uploaded_file = st.file_uploader(
    "Choose an image of a historical artifact...",
    type=["jpg", "jpeg", "png"]
)
# Step 5.3: Show Uploaded Image
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
# Step 5.4: Generate Button & Prompt
submit = st.button("Generate Artifact Description")

input_prompt = """
You are a historian. Analyze the historical artifact in the image and provide:
- Name of the artifact
- Origin
- Historical significance
- Approximate time period
"""
# Step 5.5: Generate Output
if submit:
    try:
        response = get_gemini_response(input_text, input_prompt)

        st.subheader("📜 Description of the Artifact:")
        st.write(response)
    except Exception as e:
        st.error(f"Error: {str(e)}")

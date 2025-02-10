import streamlit as st
import pytesseract
import shutil
from PIL import Image
from pdf2image import convert_from_bytes

pytesseract.pytesseract.tesseract_cmd = None
progress_text = "Operation in progress. Please wait."


# Search for Tesseract binary in PATH
@st.cache_resource
def find_tesseract_binary() -> str:
    return shutil.which("tesseract")


# Set Tesseract binary path
pytesseract.pytesseract.tesseract_cmd = find_tesseract_binary()
if pytesseract.pytesseract.tesseract_cmd:
    st.write(
        "Installed Tesseract version:", pytesseract.pytesseract.get_tesseract_version()
    )
else:
    st.error("Tesseract binary not found in PATH. Please install Tesseract.")


# Extract text from PDF and update progress bar
def extract_text_from_pdf(pdf_data):
    pages = convert_from_bytes(pdf_data, 500)  # Convert PDF to images
    total_pages = len(pages)  # Total number of pages
    text = []

    for i, page in enumerate(pages):
        text.append(pytesseract.image_to_string(page, lang="rus"))
        
        # Update progress bar
        progress = (i + 1) / total_pages  # Calculate progress percentage
        my_bar.progress(progress, text=f"{progress_text} ({i + 1}/{total_pages})")

    return text


if __name__ == "__main__":
    st.title("PDF to Text Conversion")
    uploaded_file = st.file_uploader(
        "Choose a file", type=["jpg", "jpeg", "png", "pdf", "tiff"]
    )

    if uploaded_file is not None:
        my_bar = st.progress(0, text=progress_text)
        text = extract_text_from_pdf(uploaded_file.read())

        my_bar.empty()  # Clear the progress bar after processing

        if text:
            for i, page in enumerate(text):
                st.subheader(f"Page {i + 1}")
                st.write(page)

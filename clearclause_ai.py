import streamlit as st
import fitz  # PyMuPDF for PDF handling
from transformers import pipeline

# Load summarizer model (HuggingFace)
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_summarizer()

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function to detect risks
def detect_risks(text):
    risks = []
    keywords = ["data sharing", "third party", "advertiser", "charges", "auto-renew", "subscription", "sell your data"]
    for k in keywords:
        if k.lower() in text.lower():
            risks.append(k)
    return risks

# Streamlit UI
st.title("📜 ClearClause AI - Prototype")
st.write("Upload a Terms & Conditions PDF or paste text, and get a simple summary + risk highlights.")

option = st.radio("Choose input method:", ["Paste Text", "Upload PDF"])

input_text = ""
if option == "Paste Text":
    input_text = st.text_area("Paste your Terms & Conditions text here:", height=200)
elif option == "Upload PDF":
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    if uploaded_file is not None:
        input_text = extract_text_from_pdf(uploaded_file)

if st.button("Simplify Now"):
    if input_text.strip():
        with st.spinner("Summarizing..."):
            summary = summarizer(input_text[:1000], max_length=150, min_length=50, do_sample=False)[0]['summary_text']
            risks = detect_risks(input_text)
        
        st.subheader("✅ Simplified Summary")
        st.write(summary)

        st.subheader("⚠️ Highlighted Risks")
        if risks:
            for r in risks:
                st.write(f"- {r}")
        else:
            st.write("No major risks detected.")
    else:
        st.warning("Please enter text or upload a PDF first.")

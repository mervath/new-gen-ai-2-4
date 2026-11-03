from dotenv import load_dotenv
load_dotenv()
import os
import streamlit as st
from openai import OpenAI, AuthenticationError
import fitz  # PyMuPDF for PDF
from docx import Document

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # 🔁 Replace with your actual key


# Extract text from supported file types
def extract_text(file):
    if file.type == "application/pdf":
        doc = fitz.open(stream=file.read(), filetype="pdf")
        return "\n".join([page.get_text() for page in doc])
    elif file.type == "text/plain":
        return file.read().decode("utf-8")
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return ""


# Generate question paper using GPT
def generate_question_paper(content, syllabus, pattern, difficulty, instructions):
    prompt = f"""
You are an expert exam paper setter.

SET A QUESTION PAPER based on the given study material{'' if not syllabus else ' and syllabus'}.

### STUDY MATERIAL:
{content}

### SYLLABUS:
{syllabus if syllabus else 'Not Provided'}

### PAPER PATTERN:
{pattern}

### DIFFICULTY LEVEL:
{difficulty}

### ADDITIONAL INSTRUCTIONS:
{instructions}

Ensure questions are well-phrased, diverse, and aligned with the selected difficulty and pattern.
Clearly format Part A and Part B if both are present.
Return only the question paper.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content

    except AuthenticationError:
        return "❌ Invalid API key. Please check your OpenAI API key."
    except Exception as e:
        return f"⚠️ An error occurred: {e}"


# ================= Streamlit UI ====================

st.set_page_config(page_title="SASTRA Exam Paper Setter", page_icon="📝")
st.title("📝 SASTRA Exam Paper Setter")
st.markdown("Set quality question papers automatically using AI.")

# Upload study material
study_file = st.file_uploader("📚 Upload Study Material (PDF, TXT, DOCX)", type=["pdf", "txt", "docx"])
syllabus_file = st.file_uploader("🗂️ Upload Syllabus (Optional)", type=["pdf", "txt", "docx"])

# Paper pattern
pattern = st.radio("📋 Choose Paper Pattern", (
    "Part A: 10 questions × 2 marks, Part B: 3 questions × 10 marks",
    "Part A: 5 questions × 10 marks"
))

# Difficulty
difficulty = st.selectbox("🎯 Select Difficulty Level", ["Easy", "Medium", "Hard", "Mixed"])

# Additional Instructions
instructions = st.text_area("🛠️ Additional Instructions (Optional)", placeholder="E.g., Include questions from all chapters, Bloom’s taxonomy-based, etc.")

# Generate button
if st.button("Generate Question Paper"):
    if not study_file:
        st.error("Please upload study material.")
    else:
        with st.spinner("Generating question paper..."):
            study_text = extract_text(study_file)
            syllabus_text = extract_text(syllabus_file) if syllabus_file else ""
            result = generate_question_paper(study_text, syllabus_text, pattern, difficulty, instructions)

            if result.startswith("❌") or result.startswith("⚠️"):
                st.error(result)
            else:
                st.success("✅ Question paper generated!")
                st.download_button("📥 Download Question Paper", result, file_name="question_paper.txt")
                st.text_area("📄 Preview", result, height=400)





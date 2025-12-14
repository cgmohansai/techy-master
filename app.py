import streamlit as st
from google import genai
import PyPDF2

# Create Gemini client (NEW SDK way)
client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

# Extract text from PDF
def input_pdf_text(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted
    return text

# Get response from Gemini
def get_gemini_response(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

# Streamlit UI
st.set_page_config(page_title="MockMate", page_icon="💼")
st.title("💼 MockMate: AI Interview Coach")
st.subheader("Upload your resume, and let Gemini interview you.")

with st.sidebar:
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    job_role = st.text_input("Target Job Role")
    difficulty = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Hard"])
    submit_button = st.button("Generate Interview Questions")

if submit_button and uploaded_file:
    resume_text = input_pdf_text(uploaded_file)

    prompt = f"""
    Act as a strict technical interviewer.
    The candidate is applying for the role of {job_role}.
    Resume content:
    {resume_text}

    Difficulty level: {difficulty}
    Generate 5 technical interview questions.
    Do NOT include answers.
    """

    with st.spinner("Analyzing resume..."):
        questions = get_gemini_response(prompt)
        st.success("Questions generated!")
        st.write(questions)
        st.session_state["questions"] = questions

if "questions" in st.session_state:
    st.divider()
    user_answer = st.text_area("Type your answers here", height=200)
    evaluate_button = st.button("Evaluate My Answers")

    if evaluate_button:
        eval_prompt = f"""
        Questions:
        {st.session_state['questions']}

        Candidate Answers:
        {user_answer}

        Evaluate the answers.
        Give score /10 and improvements.
        """

        with st.spinner("Evaluating..."):
            feedback = get_gemini_response(eval_prompt)
            st.write(feedback)
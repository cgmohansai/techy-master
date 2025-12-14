import streamlit as st
import google.generativeai as genai
import PyPDF2

# 1. Configure Google Gemini
# Replace 'YOUR_API_KEY' with the actual key you got from Google AI Studio
genai.configure(api_key="AIzaSyCk9NWeREdZSXunPXlXlOq6-NXlhEBUB38")

# Function to extract text from PDF Resume
def input_pdf_text(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text()
    return text

# Function to get response from Gemini
def get_gemini_response(input_prompt):
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(input_prompt)
    return response.text

# 2. The Streamlit UI Setup
st.set_page_config(page_title="MockMate", page_icon="💼")
st.title("💼 MockMate: AI Interview Coach")
st.subheader("Upload your resume, and let Google Gemini interview you.")

# Sidebar for inputs
with st.sidebar:
    st.header("Settings")
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    job_role = st.text_input("Target Job Role (e.g., Java Developer)")
    difficulty = st.selectbox("Difficulty Level", ["Beginner", "Intermediate", "Hard"])
    submit_button = st.button("Generate Interview Questions")

# 3. Main Logic
if submit_button and uploaded_file is not None:
    # Extract text from the PDF
    resume_text = input_pdf_text(uploaded_file)
    
    # Create the Prompt for Gemini
    prompt = f"""
    Act as a strict technical interviewer. 
    The candidate is applying for the role of {job_role}.
    Here is their resume content: {resume_text}
    
    Based on the resume and the difficulty level '{difficulty}', 
    generate 5 specific technical interview questions. 
    Do not give the answers yet. Just list the questions.
    """
    
    with st.spinner("Analyzing your resume..."):
        questions = get_gemini_response(prompt)
        st.success("Interview Questions Generated!")
        st.write(questions)
        
        # Store questions in session state (memory) to use later
        st.session_state['questions'] = questions

# Section to answer
if 'questions' in st.session_state:
    st.divider()
    user_answer = st.text_area("Type your answers here:", height=200)
    evaluate_button = st.button("Evaluate My Answers")
    
    if evaluate_button:
        eval_prompt = f"""
        You are an interviewer. 
        Questions asked: {st.session_state['questions']}
        Candidate's Answers: {user_answer}
        
        Please evaluate the answers. 
        1. Give a score out of 10.
        2. Highlight what was wrong.
        3. Provide the correct/better answer for each question.
        """
        with st.spinner("Grading your answers..."):
            feedback = get_gemini_response(eval_prompt)
            st.write(feedback)
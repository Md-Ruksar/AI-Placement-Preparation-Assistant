import streamlit as st
import re
import os
import requests
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)
else:
    client = None

HF_TOKEN = os.getenv("HF_TOKEN")


def ask_huggingface(question):
    if not HF_TOKEN:
        return None

    url = "https://router.huggingface.co/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "openai/gpt-oss-120b:fastest",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an AI Placement Preparation Assistant. "
                    "Help students with aptitude, technical interviews, "
                    "HR interviews, resumes, skills, career planning, "
                    "and placement preparation. Give clear, practical "
                    "and beginner-friendly answers."
                ),
            },
            {
                "role": "user",
                "content": question,
            },
        ],
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=60,
        )

        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]

        return None

    except Exception:
        return None

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Placement Preparation Assistant",
    page_icon="🎯",
    layout="wide"
)

# --------------------------------------------------
# QUESTION DATA
# --------------------------------------------------

aptitude_questions = {
    "Quantitative Aptitude": [
        {
            "question": "What is 20% of 250?",
            "options": ["25", "40", "50", "60"],
            "answer": "50",
            "explanation": "20% of 250 = (20/100) × 250 = 50."
        },
        {
            "question": "If a train travels 60 km in 1 hour, how far will it travel in 3 hours?",
            "options": ["120 km", "150 km", "180 km", "200 km"],
            "answer": "180 km",
            "explanation": "Distance = Speed × Time = 60 × 3 = 180 km."
        },
        {
            "question": "What is the average of 10, 20 and 30?",
            "options": ["15", "20", "25", "30"],
            "answer": "20",
            "explanation": "Average = (10 + 20 + 30) / 3 = 20."
        }
    ],

    "Logical Reasoning": [
        {
            "question": "Find the next number: 2, 4, 6, 8, ?",
            "options": ["9", "10", "11", "12"],
            "answer": "10",
            "explanation": "Each number increases by 2."
        },
        {
            "question": "If CAT is coded as DBU, how is DOG coded?",
            "options": ["EPH", "EOG", "DPH", "FPH"],
            "answer": "EPH",
            "explanation": "Each letter is shifted one position forward."
        },
        {
            "question": "Which one is different?",
            "options": ["Apple", "Mango", "Carrot", "Banana"],
            "answer": "Carrot",
            "explanation": "Carrot is a vegetable; the others are fruits."
        }
    ],

    "Verbal Ability": [
        {
            "question": "Choose the synonym of 'Happy'.",
            "options": ["Sad", "Joyful", "Angry", "Tired"],
            "answer": "Joyful",
            "explanation": "Joyful means happy."
        },
        {
            "question": "Choose the correct sentence.",
            "options": [
                "She go to college.",
                "She goes to college.",
                "She going college.",
                "She gone to college."
            ],
            "answer": "She goes to college.",
            "explanation": "The correct third-person singular form is 'goes'."
        },
        {
            "question": "Choose the antonym of 'Strong'.",
            "options": ["Powerful", "Weak", "Brave", "Healthy"],
            "answer": "Weak",
            "explanation": "Weak is the opposite of strong."
        }
    ]
}


technical_questions = {
    "Python": [
        {
            "question": "Which keyword is used to define a function in Python?",
            "options": ["function", "def", "fun", "define"],
            "answer": "def",
            "explanation": "Python uses the 'def' keyword to define a function."
        },
        {
            "question": "Which data type stores key-value pairs?",
            "options": ["List", "Tuple", "Dictionary", "Set"],
            "answer": "Dictionary",
            "explanation": "A dictionary stores data in key-value pairs."
        },
        {
            "question": "Which symbol is used for comments in Python?",
            "options": ["//", "#", "/*", "--"],
            "answer": "#",
            "explanation": "Python uses # for single-line comments."
        }
    ],

    "OOP": [
        {
            "question": "What does OOP stand for?",
            "options": [
                "Object Oriented Programming",
                "Object Operating Program",
                "Open Object Programming",
                "Operational Object Process"
            ],
            "answer": "Object Oriented Programming",
            "explanation": "OOP stands for Object Oriented Programming."
        },
        {
            "question": "Which concept allows a class to inherit properties from another class?",
            "options": [
                "Encapsulation",
                "Inheritance",
                "Abstraction",
                "Polymorphism"
            ],
            "answer": "Inheritance",
            "explanation": "Inheritance allows one class to acquire properties and methods of another class."
        },
        {
            "question": "Which concept hides internal implementation details?",
            "options": [
                "Inheritance",
                "Polymorphism",
                "Abstraction",
                "Compilation"
            ],
            "answer": "Abstraction",
            "explanation": "Abstraction hides unnecessary implementation details."
        }
    ],

    "DBMS": [
        {
            "question": "What does DBMS stand for?",
            "options": [
                "Database Management System",
                "Data Backup Management System",
                "Database Machine System",
                "Data Management Software"
            ],
            "answer": "Database Management System",
            "explanation": "DBMS stands for Database Management System."
        },
        {
            "question": "Which SQL command is used to retrieve data?",
            "options": ["INSERT", "UPDATE", "SELECT", "DELETE"],
            "answer": "SELECT",
            "explanation": "SELECT is used to retrieve data from a database."
        },
        {
            "question": "Which key uniquely identifies a record?",
            "options": [
                "Foreign Key",
                "Primary Key",
                "Candidate Key",
                "Composite Key"
            ],
            "answer": "Primary Key",
            "explanation": "A primary key uniquely identifies each record."
        }
    ]
}


hr_questions = [
    {
        "question": "What is the best way to answer 'Tell me about yourself'?",
        "options": [
            "Talk only about your personal life.",
            "Give a short introduction covering education, skills, projects and career goals.",
            "Say that you have nothing to say.",
            "Give a very long life story."
        ],
        "answer": "Give a short introduction covering education, skills, projects and career goals.",
        "explanation": "A good introduction should be professional, relevant and concise."
    },
    {
        "question": "What is a good way to describe your strength?",
        "options": [
            "Give a relevant strength with an example.",
            "Say you have no strengths.",
            "Mention unrelated personal information.",
            "Say that you are perfect."
        ],
        "answer": "Give a relevant strength with an example.",
        "explanation": "Examples make your answer more credible."
    },
    {
        "question": "How should you answer a question about your weakness?",
        "options": [
            "Say you have no weakness.",
            "Mention a genuine weakness and explain how you are improving it.",
            "Blame other people.",
            "Avoid answering completely."
        ],
        "answer": "Mention a genuine weakness and explain how you are improving it.",
        "explanation": "This shows self-awareness and willingness to improve."
    },
    {
        "question": "What should you do before attending an interview?",
        "options": [
            "Research the company and role.",
            "Do nothing.",
            "Memorize random answers.",
            "Avoid learning about the company."
        ],
        "answer": "Research the company and role.",
        "explanation": "Understanding the company and role helps you give relevant answers."
    },
    {
        "question": "What should you do if you don't know the answer to an interview question?",
        "options": [
            "Make up an answer.",
            "Politely admit that you don't know and show willingness to learn.",
            "Leave the interview.",
            "Argue with the interviewer."
        ],
        "answer": "Politely admit that you don't know and show willingness to learn.",
        "explanation": "Honesty and willingness to learn are better than inventing an answer."
    }
]


mock_questions = [
    {
        "question": "What is 15% of 200?",
        "options": ["20", "25", "30", "35"],
        "answer": "30",
        "explanation": "15% of 200 = (15/100) × 200 = 30."
    },
    {
        "question": "Which keyword is used to define a function in Python?",
        "options": ["function", "def", "define", "fun"],
        "answer": "def",
        "explanation": "Python uses the 'def' keyword to define functions."
    },
    {
        "question": "What does OOP stand for?",
        "options": [
            "Object Oriented Programming",
            "Object Operating Program",
            "Open Object Programming",
            "Operational Object Process"
        ],
        "answer": "Object Oriented Programming",
        "explanation": "OOP stands for Object Oriented Programming."
    },
    {
        "question": "Which SQL command retrieves data from a database?",
        "options": ["INSERT", "SELECT", "UPDATE", "DELETE"],
        "answer": "SELECT",
        "explanation": "SELECT is used to retrieve records from a database."
    },
    {
        "question": "What is a good way to answer 'Tell me about yourself'?",
        "options": [
            "Give a short professional introduction.",
            "Talk only about hobbies.",
            "Give a very long personal story.",
            "Say nothing."
        ],
        "answer": "Give a short professional introduction.",
        "explanation": "A good introduction should briefly cover your education, skills, projects and career goals."
    }
]


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "aptitude_score" not in st.session_state:
    st.session_state.aptitude_score = 0

if "aptitude_attempted" not in st.session_state:
    st.session_state.aptitude_attempted = 0

if "aptitude_index" not in st.session_state:
    st.session_state.aptitude_index = 0


if "technical_score" not in st.session_state:
    st.session_state.technical_score = 0

if "technical_attempted" not in st.session_state:
    st.session_state.technical_attempted = 0

if "technical_index" not in st.session_state:
    st.session_state.technical_index = 0


if "hr_score" not in st.session_state:
    st.session_state.hr_score = 0

if "hr_attempted" not in st.session_state:
    st.session_state.hr_attempted = 0

if "hr_index" not in st.session_state:
    st.session_state.hr_index = 0


if "mock_score" not in st.session_state:
    st.session_state.mock_score = 0

if "mock_attempted" not in st.session_state:
    st.session_state.mock_attempted = 0

if "mock_index" not in st.session_state:
    st.session_state.mock_index = 0


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("Placement Assistant")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Aptitude Practice",
        "Technical Interview",
        "HR Interview",
        "Mock Interview",
        "Resume Analysis",
        "Skill Gap Analysis",
        "AI Career Assistant"
    ]
)


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if page == "Dashboard":

    st.title("AI Placement Preparation Assistant")
    st.subheader("Dashboard")

    total_attempted = (
        st.session_state.aptitude_attempted
        + st.session_state.technical_attempted
        + st.session_state.hr_attempted
        + st.session_state.mock_attempted
    )

    total_score = (
        st.session_state.aptitude_score
        + st.session_state.technical_score
        + st.session_state.hr_score
        + st.session_state.mock_score
    )

    if total_attempted > 0:
        overall_score = (total_score / total_attempted) * 100
    else:
        overall_score = 0

    progress = min(total_attempted * 5, 100)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Questions Attempted", total_attempted)

    with col2:
        st.metric("Overall Score", f"{overall_score:.0f}%")

    with col3:
        st.metric("Progress", f"{progress}%")

    with col4:
        st.metric("Skills Improved", 0)

    st.divider()

    st.subheader("Preparation Modules")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("### Aptitude")
        st.write("Practice quantitative, logical and verbal questions.")

    with col2:
        st.write("### Technical")
        st.write("Practice Python, OOP and DBMS questions.")

    with col3:
        st.write("### HR Interview")
        st.write("Practice common HR interview questions.")

    st.divider()

    st.subheader("More Modules")

    st.write("Mock Interview is now available.")

    st.write("Resume Analysis — Coming soon")
    st.write("Skill Gap Analysis — Coming soon")
    st.write("AI Career Assistant — Coming soon")


# --------------------------------------------------
# APTITUDE PRACTICE
# --------------------------------------------------

elif page == "Aptitude Practice":

    st.title("Aptitude Practice")

    topic = st.selectbox(
        "Select Topic",
        list(aptitude_questions.keys())
    )

    questions = aptitude_questions[topic]

    question_index = st.session_state.aptitude_index % len(questions)

    current_question = questions[question_index]

    st.subheader(
        f"Question {question_index + 1} of {len(questions)}"
    )

    st.write(current_question["question"])

    selected_answer = st.radio(
        "Choose your answer:",
        current_question["options"],
        key=f"aptitude_{topic}_{question_index}"
    )

    if st.button("Submit Answer", key="aptitude_submit"):

        st.session_state.aptitude_attempted += 1

        if selected_answer == current_question["answer"]:
            st.session_state.aptitude_score += 1
            st.success("Correct!")
        else:
            st.error(
                f"Incorrect. Correct answer: {current_question['answer']}"
            )

        st.info(current_question["explanation"])

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Next Question", key="aptitude_next"):
            st.session_state.aptitude_index += 1
            st.rerun()

    with col2:
        if st.button("Reset Aptitude Score", key="aptitude_reset"):
            st.session_state.aptitude_score = 0
            st.session_state.aptitude_attempted = 0
            st.session_state.aptitude_index = 0
            st.rerun()

    st.write(
        f"Score: {st.session_state.aptitude_score} / "
        f"{st.session_state.aptitude_attempted}"
    )


# --------------------------------------------------
# TECHNICAL INTERVIEW
# --------------------------------------------------

elif page == "Technical Interview":

    st.title("Technical Interview")

    topic = st.selectbox(
        "Select Topic",
        list(technical_questions.keys())
    )

    questions = technical_questions[topic]

    question_index = st.session_state.technical_index % len(questions)

    current_question = questions[question_index]

    st.subheader(
        f"Question {question_index + 1} of {len(questions)}"
    )

    st.write(current_question["question"])

    selected_answer = st.radio(
        "Choose your answer:",
        current_question["options"],
        key=f"technical_{topic}_{question_index}"
    )

    if st.button("Submit Answer", key="technical_submit"):

        st.session_state.technical_attempted += 1

        if selected_answer == current_question["answer"]:
            st.session_state.technical_score += 1
            st.success("Correct!")
        else:
            st.error(
                f"Incorrect. Correct answer: {current_question['answer']}"
            )

        st.info(current_question["explanation"])

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Next Technical Question", key="technical_next"):
            st.session_state.technical_index += 1
            st.rerun()

    with col2:
        if st.button("Reset Technical Score", key="technical_reset"):
            st.session_state.technical_score = 0
            st.session_state.technical_attempted = 0
            st.session_state.technical_index = 0
            st.rerun()

    st.write(
        f"Score: {st.session_state.technical_score} / "
        f"{st.session_state.technical_attempted}"
    )


# --------------------------------------------------
# HR INTERVIEW
# --------------------------------------------------

elif page == "HR Interview":

    st.title("HR Interview")

    question_index = (
        st.session_state.hr_index % len(hr_questions)
    )

    current_question = hr_questions[question_index]

    st.subheader(
        f"Question {question_index + 1} of {len(hr_questions)}"
    )

    st.write(current_question["question"])

    selected_answer = st.radio(
        "Choose your answer:",
        current_question["options"],
        key=f"hr_{question_index}"
    )

    if st.button("Submit HR Answer", key="hr_submit"):

        st.session_state.hr_attempted += 1

        if selected_answer == current_question["answer"]:
            st.session_state.hr_score += 1
            st.success("Correct!")
        else:
            st.error(
                f"Incorrect. Correct answer: {current_question['answer']}"
            )

        st.info(current_question["explanation"])

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Next HR Question", key="hr_next"):
            st.session_state.hr_index += 1
            st.rerun()

    with col2:
        if st.button("Reset HR Score", key="hr_reset"):
            st.session_state.hr_score = 0
            st.session_state.hr_attempted = 0
            st.session_state.hr_index = 0
            st.rerun()

    st.write(
        f"Score: {st.session_state.hr_score} / "
        f"{st.session_state.hr_attempted}"
    )


# --------------------------------------------------
# MOCK INTERVIEW
# --------------------------------------------------

elif page == "Mock Interview":

    st.title("Mock Interview")

    st.write(
        "Simulate a short placement interview covering aptitude, "
        "technical and HR questions."
    )

    st.divider()

    question_index = (
        st.session_state.mock_index % len(mock_questions)
    )

    current_question = mock_questions[question_index]

    st.subheader(
        f"Interview Question {question_index + 1} "
        f"of {len(mock_questions)}"
    )

    st.write(current_question["question"])

    selected_answer = st.radio(
        "Choose your answer:",
        current_question["options"],
        key=f"mock_{question_index}"
    )

    if st.button("Submit Interview Answer", key="mock_submit"):

        st.session_state.mock_attempted += 1

        if selected_answer == current_question["answer"]:
            st.session_state.mock_score += 1
            st.success("Correct!")
        else:
            st.error(
                f"Incorrect. Correct answer: {current_question['answer']}"
            )

        st.info(current_question["explanation"])

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Next Interview Question", key="mock_next"):
            st.session_state.mock_index += 1
            st.rerun()

    with col2:
        if st.button("Reset Mock Interview", key="mock_reset"):
            st.session_state.mock_score = 0
            st.session_state.mock_attempted = 0
            st.session_state.mock_index = 0
            st.rerun()

    st.divider()

    if st.session_state.mock_attempted > 0:

        mock_percentage = (
            st.session_state.mock_score
            / st.session_state.mock_attempted
        ) * 100

        st.subheader("Current Interview Performance")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Score",
                f"{st.session_state.mock_score} / "
                f"{st.session_state.mock_attempted}"
            )

        with col2:
            st.metric(
                "Accuracy",
                f"{mock_percentage:.0f}%"
            )

        if mock_percentage >= 80:
            st.success("Excellent performance!")

        elif mock_percentage >= 60:
            st.warning("Good performance. Keep practicing.")

        else:
            st.error("More practice is recommended.")

# --------------------------------------------------
# RESUME ANALYSIS
# --------------------------------------------------

elif page == "Resume Analysis":

    st.title("Resume Analysis")

    st.write(
        "Upload your resume to extract basic information "
        "and prepare it for analysis."
    )

    st.divider()

    uploaded_file = st.file_uploader(
        "Upload your Resume",
        type=["pdf", "txt"]
    )

    if uploaded_file is not None:

        st.success(f"Resume uploaded: {uploaded_file.name}")

        if uploaded_file.type == "text/plain":

            resume_text = uploaded_file.read().decode(
                "utf-8",
                errors="ignore"
            )

            st.subheader("Extracted Resume Text")

            st.text_area(
                "Resume Content",
                resume_text,
                height=300
            )

            word_count = len(resume_text.split())

            st.write(f"Word Count: {word_count}")

        else:

            st.info(
                "PDF uploaded successfully. "
                "PDF text extraction will be added in the next stage."
            )

        st.divider()

        st.subheader("Resume Analysis")

        st.write("Skills Detection — Coming soon")
        st.write("Experience Analysis — Coming soon")
        st.write("Education Analysis — Coming soon")
        st.write("Resume Score — Coming soon")
        st.write("Improvement Suggestions — Coming soon")
# --------------------------------------------------
# SKILL GAP ANALYSIS
# --------------------------------------------------

elif page == "Skill Gap Analysis":

    st.title("Skill Gap Analysis")

    st.write(
        "Analyze your current preparation performance "
        "and identify areas that need improvement."
    )

    st.divider()

    # Calculate individual performance

    if st.session_state.aptitude_attempted > 0:
        aptitude_percentage = (
            st.session_state.aptitude_score
            / st.session_state.aptitude_attempted
        ) * 100
    else:
        aptitude_percentage = 0

    if st.session_state.technical_attempted > 0:
        technical_percentage = (
            st.session_state.technical_score
            / st.session_state.technical_attempted
        ) * 100
    else:
        technical_percentage = 0

    if st.session_state.hr_attempted > 0:
        hr_percentage = (
            st.session_state.hr_score
            / st.session_state.hr_attempted
        ) * 100
    else:
        hr_percentage = 0

    if st.session_state.mock_attempted > 0:
        mock_percentage = (
            st.session_state.mock_score
            / st.session_state.mock_attempted
        ) * 100
    else:
        mock_percentage = 0

    # Display performance

    st.subheader("Your Performance")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Aptitude",
            f"{aptitude_percentage:.0f}%"
        )

        st.metric(
            "Technical",
            f"{technical_percentage:.0f}%"
        )

    with col2:
        st.metric(
            "HR Interview",
            f"{hr_percentage:.0f}%"
        )

        st.metric(
            "Mock Interview",
            f"{mock_percentage:.0f}%"
        )

    st.divider()

    # Identify skill gaps

    st.subheader("Skill Gap Report")

    performance = {
        "Aptitude": aptitude_percentage,
        "Technical": technical_percentage,
        "HR Interview": hr_percentage,
        "Mock Interview": mock_percentage
    }

    for skill, score in performance.items():

        if score == 0:
            st.info(
                f"{skill}: Not enough data yet. "
                "Attempt some questions to generate a result."
            )

        elif score < 50:
            st.error(
                f"{skill}: Needs significant improvement."
            )

        elif score < 75:
            st.warning(
                f"{skill}: Needs more practice."
            )

        else:
            st.success(
                f"{skill}: Good performance."
            )

    st.divider()

    # Recommendations

    st.subheader("Recommended Focus Areas")

    weak_skills = [
        skill
        for skill, score in performance.items()
        if 0 < score < 75
    ]

    if weak_skills:

        st.write(
            "Based on your current performance, focus on:"
        )

        for skill in weak_skills:
            st.write(f"- {skill}")

    else:

        st.success(
            "No major skill gaps detected from your current attempts."
        )

    st.divider()

    st.caption(
        "The current analysis is based on your practice scores. "
        "AI-powered personalized recommendations will be added later."
    )

# --------------------------------------------------
# AI CAREER ASSISTANT
# --------------------------------------------------

elif page == "AI Career Assistant":

    st.title("AI Career Assistant")

    st.write(
        "Ask questions about placement preparation, "
        "interviews, skills, career planning and learning."
    )

    st.divider()

    if "career_messages" not in st.session_state:
        st.session_state.career_messages = []

    # Display previous messages

    for message in st.session_state.career_messages:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input

    user_question = st.chat_input(
        "Ask your career question..."
    )

    if user_question:

        st.session_state.career_messages.append(
            {
                "role": "user",
                "content": user_question
            }
        )

        with st.chat_message("user"):
            st.write(user_question)

        # Generate AI response

        try:
            if client:
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=user_question
                )
                assistant_response = response.text
            else:
                raise Exception("Gemini client not available")

        except Exception:
            assistant_response = ask_huggingface(user_question)

            if not assistant_response:
                assistant_response = (
                    "The AI services are temporarily unavailable. "
                    "Please try again in a few seconds."
                )

        st.session_state.career_messages.append(
            {
                "role": "assistant",
                "content": assistant_response
            }
        )

        with st.chat_message("assistant"):
            st.write(assistant_response)

import streamlit as st
import json
import random

# Load questions from JSON
with open("merged_chapters.json", "r") as f:
    questions_by_chapter = json.load(f)

# App title
st.title("🧠 HR Quiz App")

# Sidebar - Chapter selection and score
st.sidebar.header("Quiz Settings")
selected_chapters = st.sidebar.multiselect(
    "Select Chapters to Practice",
    options=list(questions_by_chapter.keys()),
    default=list(questions_by_chapter.keys())
)

# Function to flatten questions from selected chapters
def get_filtered_questions(chapters):
    question_pool = []
    for chapter in chapters:
        question_pool.extend(questions_by_chapter.get(chapter, []))
    random.shuffle(question_pool)
    return question_pool

# Initialize session state
if "questions" not in st.session_state:
    st.session_state.questions = get_filtered_questions(selected_chapters)
    st.session_state.index = 0
    st.session_state.correct = 0
    st.session_state.incorrect = 0
    st.session_state.answered = False
    st.session_state.score_history = []

# Restart button
if st.sidebar.button("🔁 Restart Quiz"):
    st.session_state.questions = get_filtered_questions(selected_chapters)
    st.session_state.index = 0
    st.session_state.correct = 0
    st.session_state.incorrect = 0
    st.session_state.answered = False
    st.session_state.score_history = []

# Display current question
if st.session_state.index < len(st.session_state.questions):
    question_obj = st.session_state.questions[st.session_state.index]
    st.markdown(f"**Question {st.session_state.index + 1} of {len(st.session_state.questions)}**")
    st.write(question_obj["question"])
    user_answer = st.radio("Choose your answer:", question_obj["options"], key=st.session_state.index)

    if st.button("✅ Submit Answer"):
        if not st.session_state.answered:
            if user_answer == question_obj["answer"]:
                st.success("Correct!")
                st.session_state.correct += 1
            else:
                st.error(f"Incorrect. The correct answer is: {question_obj['answer']}")
                st.session_state.incorrect += 1
            st.session_state.answered = True

    if st.session_state.answered and st.button("➡️ Next Question"):
        st.session_state.index += 1
        st.session_state.answered = False

    # Show progress
    total_attempted = st.session_state.correct + st.session_state.incorrect
    st.progress(total_attempted / len(st.session_state.questions))
    st.sidebar.markdown(f"**Progress:** {total_attempted} / {len(st.session_state.questions)}")
    st.sidebar.markdown(f"✅ Correct: {st.session_state.correct}")
    st.sidebar.markdown(f"❌ Incorrect: {st.session_state.incorrect}")
    if total_attempted > 0:
        score_percent = (st.session_state.correct / total_attempted) * 100
        st.sidebar.markdown(f"📊 Score: {score_percent:.1f}%")

else:
    st.success("🎉 You've completed the quiz!")
    st.balloons()
    st.markdown(f"**Final Score: {st.session_state.correct} correct, {st.session_state.incorrect} incorrect**")
    if st.button("🔁 Restart Quiz"):
        st.session_state.questions = get_filtered_questions(selected_chapters)
        st.session_state.index = 0
        st.session_state.correct = 0
        st.session_state.incorrect = 0
        st.session_state.answered = False

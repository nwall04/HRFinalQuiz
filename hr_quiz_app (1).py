
import streamlit as st
import json
import random

# Load questions from JSON
with open("merged_chapters.json", "r") as f:
    raw_data = json.load(f)

# Extract simplified chapter names and map to full
chapter_name_map = {f"Chapter {ch.split()[1]}": ch for ch in raw_data.keys()}
chapter_display_names = list(chapter_name_map.keys())

# Sidebar - Chapter selection and score
st.sidebar.header("Quiz Settings")
selected_short_names = st.sidebar.multiselect(
    "Select Chapters to Practice",
    options=chapter_display_names,
    default=chapter_display_names
)

selected_chapters = [chapter_name_map[name] for name in selected_short_names]

# Flatten questions from selected chapters
def get_filtered_questions(chapters):
    question_pool = []
    for chapter in chapters:
        chapter_data = raw_data.get(chapter, {})
        for q_type in ["multiple_choice", "true_false"]:
            for q in chapter_data.get(q_type, []):
                question_pool.append(q)
    random.shuffle(question_pool)
    return question_pool

# Initialize session state
if "questions" not in st.session_state:
    st.session_state.questions = get_filtered_questions(selected_chapters)
    st.session_state.index = 0
    st.session_state.correct = 0
    st.session_state.incorrect = 0
    st.session_state.answered = False

# Restart button
if st.sidebar.button("🔁 Restart Quiz"):
    st.session_state.questions = get_filtered_questions(selected_chapters)
    st.session_state.index = 0
    st.session_state.correct = 0
    st.session_state.incorrect = 0
    st.session_state.answered = False

# Display current question
if st.session_state.index < len(st.session_state.questions):
    question_obj = st.session_state.questions[st.session_state.index]
    question_text = question_obj.get("question", "")
    options = question_obj.get("options", [])
    answer = question_obj.get("answer", "")

    st.markdown(f"**Question {st.session_state.index + 1} of {len(st.session_state.questions)}**")
    st.write(question_text)
    user_answer = st.radio("Choose your answer:", options, key=st.session_state.index)

    if st.button("✅ Submit Answer"):
        if not st.session_state.answered:
            if user_answer == answer:
                st.success("Correct!")
                st.session_state.correct += 1
            else:
                st.error(f"Incorrect. The correct answer is: {answer}")
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

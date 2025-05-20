import streamlit as st

# Hàm phản hồi chatbot (logic mẫu, bạn có thể thay bằng API GPT hoặc xử lý riêng)
def get_bot_response(user_input):
    user_input = user_input.lower()
    if "hello" in user_input or "hi" in user_input:
        return "Hello! How can I help you today?"
    elif "bye" in user_input:
        return "Goodbye! Have a nice day!"
    else:
        return f"You said: {user_input}"

# --- Giao diện ---
st.set_page_config(page_title="Chatbot Test", layout="centered")
st.title("🤖 Simple Chatbot Demo")

# Lưu lịch sử hội thoại trong session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Nhập liệu từ người dùng
user_input = st.text_input("You:", key="input")

# Khi có input, xử lý và hiển thị phản hồi
if user_input:
    bot_response = get_bot_response(user_input)

    # Lưu vào lịch sử chat
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Bot", bot_response))

# Hiển thị hội thoại
for speaker, message in st.session_state.chat_history:
    if speaker == "You":
        st.markdown(f"**🧑‍💻 {speaker}:** {message}")
    else:
        st.markdown(f"**🤖 {speaker}:** {message}")

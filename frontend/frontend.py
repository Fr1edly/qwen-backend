import streamlit as st
import requests

# Заголовок приложения
st.title("Code Chat Bot")

# Текстовая область для пользовательского ввода
user_input = st.text_area("Введите ваш запрос:", height=150)

# Отправка запроса на бэкенд
if st.button("Отправить"):
    if not user_input.strip():
        st.warning("Введите сообщение для отправки!")
    else:
        with st.spinner("Обрабатываем запрос..."):
            try:
                # Отправляем запрос на бэкенд
                response = requests.post(
                    "http://localhost:5000/chat",
                    json={"message": user_input}
                )
                # Обрабатываем ответ
                if response.status_code == 200:
                    bot_response = response.json().get("response", "Нет ответа")
                    # Проверка на наличие кода
                    if bot_response.startswith("```"):
                        code = bot_response.replace("```", "").strip()
                        st.code(code, language="python")  # Подсветка синтаксиса Python
                    else:
                        st.text_area("Ответ бота:", value=bot_response, height=150)
                else:
                    st.error(f"Ошибка сервера: {response.status_code}")
            except Exception as e:
                st.error(f"Ошибка соединения с сервером: {e}")

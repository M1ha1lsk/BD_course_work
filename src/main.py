import streamlit as st

# Главная логика приложения
def main():
    school_name = st.session_state.get('school_name', None)

    if not school_name:
        st.error("вы не вошли в систему")
        return
    
    if school_name:
        st.success(f"{school_name}, вы успешно вошли!")

if __name__ == "__main__":
    main()

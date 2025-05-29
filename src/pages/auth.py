import streamlit as st
import psycopg2
from repositories.school import get_school_id_by_name
from repositories.regions import get_region_id
from repositories.regions import get_all_regions
from repositories.redis_repository import RedisRepository
redis_repo = RedisRepository()
import bcrypt
from settings import DB_CONFIG

# Хеширование пароля
def hash_password(password):
    salt = bcrypt.gensalt()  # Генерация соли
    hashed_password = (bcrypt.hashpw(password.encode('utf-8'), salt)).decode('utf-8')
    return hashed_password

# Проверка пароля
def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)

# Регистрация пользователя
def register_user(school_name, region_name, password):
    region_id = get_region_id(region_name)
    if not region_id:
        st.error("Указанный регион не найден.")
        return False

    hashed_password = hash_password(password)  # Хеширование пароля
    query = """
    INSERT INTO sport_schools (school_name, school_role, user_password, region_id)
    VALUES (%s, %s, %s, %s);
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (school_name, "user", hashed_password, region_id))
            conn.commit()
    st.success("Регистрация успешна! Теперь вы можете войти.")
    return True

# Авторизация пользователя
def authenticate_user(school_name, password):
    query = """
    SELECT user_password FROM sport_schools WHERE school_name = %s;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (school_name,))
            result = cur.fetchone()
            if result:
                stored_password = result[0]
                
                if isinstance(stored_password, str):
                    stored_password = stored_password.encode('utf-8')
                
                if check_password(password, stored_password):
                    school_id = get_school_id_by_name(school_name)
                    if school_id:
                        # Генерируем токен (упрощённо)
                        import uuid
                        token = str(uuid.uuid4())
                        
                        # Сохраняем в Redis
                        redis_repo.store_token(school_name, token)
                        
                        st.session_state.school_id = school_id
                        st.session_state.school_name = school_name
                        st.session_state.token = token
                        return True
    return False

# Главная функция для аутентификации и регистрации
def login_or_register():
    st.title("Добро пожаловать!")

    option = st.radio("Выберите действие:", ["Вход", "Регистрация"])

    if option == "Вход":
        school_name = st.text_input("Название спортивной школы")
        password = st.text_input("Пароль", type="password")
        login_btn = st.button("Войти")

        if login_btn:
            if authenticate_user(school_name, password):
                st.success(f"Добро пожаловать, {school_name}!")
                st.rerun()  # Перезагружаем страницу после успешного входа
            else:
                st.error("Неверное имя или пароль.")

    elif option == "Регистрация":
        school_name = st.text_input("Название спортивной школы")
        region_name = st.selectbox("Выберите регион", get_all_regions())
        password = st.text_input("Пароль", type="password")
        confirm_password = st.text_input("Подтвердите пароль", type="password")
        register_btn = st.button("Зарегистрироваться")

        if register_btn:
            if school_name.lower() == "admin":
                st.error("Имя 'admin' запрещено.")
            elif password != confirm_password:
                st.error("Пароли не совпадают.")
            elif register_user(school_name, region_name, password):
                st.rerun()  # Перезагружаем страницу после успешной регистрации

# Основная функция страницы
def main():
    school_name = st.session_state.get('school_name', None)
    token = st.session_state.get('token', None)

    if school_name and token:
        # Проверяем токен в Redis
        if redis_repo.validate_token(token):
            st.success(f"Добро пожаловать, {school_name}!")
            if st.button("Выйти"):
                redis_repo.invalidate_token(token)
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        else:
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            login_or_register()
    else:
        login_or_register()

# Запуск приложения
if __name__ == "__main__":
    main()
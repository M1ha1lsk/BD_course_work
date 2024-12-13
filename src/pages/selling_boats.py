import psycopg2
import psycopg2.extras
import streamlit as st
from repositories.boats import get_boats
from repositories.boats import start_boat_explotation
from repositories.school import get_school_role
from datetime import date
from settings import DB_CONFIG


# Функция отображения страницы продажи лодок
def show_selling_boats_page(school_name: str):
    st.title("Покупка лодок")

    if  school_name is None:
        st.error("Вы не авторизовались.")
        return
    
    # Получаем роль пользователя
    school_role = get_school_role(school_name)
    if not school_role:
        return  # Если роль не найдена, прекращаем выполнение
    
    # Получаем список лодок из базы данных
    boats = get_boats()
    boat_options = {f"{boat['firm_name']}   {boat['class']}   {boat['user_weight']}": boat['boat_id'] for boat in boats}

    # Логика выбора школ в зависимости от роли пользователя
    if school_role == "admin":
        # Если роль admin, показываем все школы
        query_schools = "SELECT school_name FROM sport_schools;"
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(query_schools)
                schools = cur.fetchall()

        school_names = [school[0] for school in schools]
    else:
        # Если роль не admin, показываем только школу пользователя
        school_names = [school_name]

    # Поля для ввода данных
    selected_boat_name = st.selectbox("Выберите лодку", list(boat_options.keys()))
    school_name = st.selectbox("Выберите школу", school_names)
    deal_date = st.date_input("Выберите дату сделки", min_value=date.today())

    # Кнопки
    add_deal_btn = st.button("Зарегистрировать сделку и начать эксплуатацию")

    # Обработчик события
    if add_deal_btn:
        boat_id = boat_options[selected_boat_name]
            
        # Добавляем запись о сделке и начинаем эксплуатацию лодки
        end_date = start_boat_explotation(boat_id, school_name, deal_date)
        query_update = """
        UPDATE boats SET purchased = TRUE WHERE boat_id = %s;
        """
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(query_update, (boat_id,))
                conn.commit()
        if end_date:
            st.success(f"Эксплуатация лодки {boat_id} началась с {deal_date}. Конец эксплуатации: {end_date}")

show_selling_boats_page(st.session_state.get('school_name', None))


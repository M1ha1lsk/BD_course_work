import streamlit as st
import psycopg2
from psycopg2 import sql
from settings import DB_CONFIG


# Функция для получения информации о лодках всех школ (для admin)
def get_all_boats_exploitation():
    query = """
    SELECT 
        boat_explotation.boat_id,
        boat_firms.firm_name,
        boat_specifications.class,
        boat_specifications.user_weight,
        boat_explotation.begin_date,
        boat_explotation.end_date,
        sport_schools.school_name
    FROM boat_explotation
    JOIN boats ON boat_explotation.boat_id = boats.boat_id
    JOIN boat_specifications ON boats.spec_id = boat_specifications.spec_id
    JOIN boat_firms ON boats.firm_id = boat_firms.firm_id
    JOIN sport_schools ON boat_explotation.school_id = sport_schools.school_id
    ORDER BY sport_schools.school_name, boat_explotation.boat_id, boat_explotation.begin_date DESC;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            result = cur.fetchall()
    return result


# Функция для получения информации о лодках школы
def get_boats_exploitation_by_school(school_id: int):
    query = """
    SELECT 
        boat_explotation.boat_id,
        boat_firms.firm_name,
        boat_specifications.class,
        boat_specifications.user_weight,
        boat_explotation.begin_date,
        boat_explotation.end_date
    FROM boat_explotation
    JOIN boats ON boat_explotation.boat_id = boats.boat_id
    JOIN boat_specifications ON boats.spec_id = boat_specifications.spec_id
    JOIN boat_firms ON boats.firm_id = boat_firms.firm_id
    WHERE boat_explotation.school_id = %s
    ORDER BY boat_explotation.begin_date DESC;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (school_id,))
            result = cur.fetchall()
    return result


# Функция для отображения страницы
def show_my_boats_page(school_name: str):
    st.title("Мои лодки")

    # Получение данных пользователя: school_id и role
    query_school_info = """
    SELECT school_id, school_role FROM sport_schools WHERE school_name = %s;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query_school_info, (school_name,))
            school_info = cur.fetchone()
    
    if not school_info:
        st.error("Школа не найдена.")
        return

    school_id, school_role = school_info  # Распаковываем school_id и роль пользователя

    # Получаем данные о лодках
    if school_role == "admin":
        boats = get_all_boats_exploitation()
        if not boats:
            st.info("В данный момент нет данных о лодках.")
            return
        
        st.subheader("Список лодок для всех школ")
        st.table(
            {
                "ID Лодки": [boat[0] for boat in boats],
                "Производитель": [boat[1] for boat in boats],
                "Класс": [boat[2] for boat in boats],
                "Вес пользователя": [boat[3] for boat in boats],
                "Дата начала эксплуатации": [boat[4] for boat in boats],
                "Дата окончания эксплуатации": [boat[5] for boat in boats],
                "Школа": [boat[6] for boat in boats],
            }
        )
    else:
        boats = get_boats_exploitation_by_school(school_id)
        if not boats:
            st.info("В данный момент нет данных о лодках для вашей школы.")
            return

        st.subheader(f"Список лодок для школы '{school_name}'")
        st.table(
            {
                "ID Лодки": [boat[0] for boat in boats],
                "Производитель": [boat[1] for boat in boats],
                "Класс": [boat[2] for boat in boats],
                "Вес пользователя": [boat[3] for boat in boats],
                "Дата начала эксплуатации": [boat[4] for boat in boats],
                "Дата окончания эксплуатации": [boat[5] for boat in boats],
            }
        )


# Отображаем страницу
show_my_boats_page(st.session_state.get('school_name', None))
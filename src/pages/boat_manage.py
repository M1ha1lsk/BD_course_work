import streamlit as st
import psycopg2
from settings import DB_CONFIG

# Функция для получения роли пользователя
def get_user_role(school_name: str):
    query = """
    SELECT school_role FROM sport_schools WHERE school_name = %s;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (school_name,))
            result = cur.fetchone()
            if result:
                return result[0]
    return None

# Функция для получения списка спецификаций лодок
def get_boat_specifications():
    query = """
    SELECT spec_id, class, weight, user_weight FROM boat_specifications;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

# Функция для получения списка производителей лодок
def get_boat_firms():
    query = """
    SELECT firm_id, firm_name FROM boat_firms;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

# Функция для добавления лодки в базу данных
def add_boat(spec_id: int, firm_id: int, price: int):
    query = """
    INSERT INTO boats (spec_id, firm_id, price, purchased)
    VALUES (%s, %s, %s, FALSE);
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (spec_id, firm_id, price))
            conn.commit()

# Функция для получения информации о лодке по boat_id
def get_boat_info(boat_id: int):
    query = """
    SELECT 
        boats.boat_id, 
        boat_specifications.class, 
        boat_specifications.weight, 
        boat_specifications.user_weight,
        boat_firms.firm_name,
        CASE WHEN boats.purchased = TRUE THEN 'Да' ELSE 'Нет' END exp
    FROM boats
    JOIN boat_specifications ON boats.spec_id = boat_specifications.spec_id
    JOIN boat_firms ON boats.firm_id = boat_firms.firm_id
    WHERE boats.boat_id = %s;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (boat_id,))
            return cur.fetchone()

# Функция для удаления лодки по boat_id
def delete_boat(boat_id: int):
    query = "DELETE FROM boats WHERE boat_id = %s;"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (boat_id,))
            conn.commit()

# Основная функция отображения страницы
def show_boats_page(school_name: str):
    st.title("Управление лодками")

    # Проверяем роль пользователя
    user_role = get_user_role(school_name)
    if user_role != "admin":
        st.error("У вас недостаточно прав для использования этой страницы.")
        return

    # Страница добавления лодок
    st.header("Добавить лодку")
    boat_specs = get_boat_specifications()
    boat_firms = get_boat_firms()

    if not boat_specs or not boat_firms:
        st.error("Не удалось загрузить данные. Проверьте таблицы в базе данных.")
        return

    # Подготавливаем выборы для спецификаций и производителей
    spec_options = {
        f"Class: {spec[1]}, Weight: {spec[2]}, User Weight: {spec[3]}": spec[0] for spec in boat_specs
    }
    firm_options = {firm[1]: firm[0] for firm in boat_firms}

    # Добавление лодки
    selected_spec = st.selectbox("Выберите спецификацию лодки", list(spec_options.keys()))
    selected_firm = st.selectbox("Выберите производителя лодки", list(firm_options.keys()))
    selected_price = st.text_input("Введите цену", key='price_input')
    add_boat_btn = st.button("Добавить лодку")

    if add_boat_btn:
        spec_id = spec_options[selected_spec]
        firm_id = firm_options[selected_firm]
        try:
            price = int(selected_price)
            add_boat(spec_id, firm_id, price)
            st.success("Лодка успешно добавлена.")
        except ValueError:
            st.error("Цена должна быть числом.")

    # Страница удаления лодок
    st.header("Удалить лодку")
    if "boat_info" not in st.session_state:
        st.session_state.boat_info = None

    boat_id = st.text_input("Введите ID лодки", key="boat_id_input")
    fetch_boat_btn = st.button("Найти лодку", key="fetch_boat_button")

    if fetch_boat_btn:
        if not boat_id.isdigit():
            st.error("ID лодки должен быть числом.")
        else:
            boat_info = get_boat_info(int(boat_id))
            if boat_info:
                st.session_state.boat_info = boat_info
                st.success("Лодка найдена.")
            else:
                st.error(f"Лодка с ID {boat_id} не найдена.")
                st.session_state.boat_info = None

    if st.session_state.boat_info:
        st.write("Информация о лодке:")
        st.table({
            "ID Лодки": [st.session_state.boat_info[0]],
            "Класс": [st.session_state.boat_info[1]],
            "Вес": [st.session_state.boat_info[2]],
            "Вес пользователя": [st.session_state.boat_info[3]],
            "Производитель": [st.session_state.boat_info[4]],
            "В эксплуатации": [st.session_state.boat_info[5]],
        })

        if st.button("Удалить лодку"):
            delete_boat(int(st.session_state.boat_info[0]))
            st.success(f"Лодка с ID {st.session_state.boat_info[0]} успешно удалена.")
            st.session_state.boat_info = None

# Отображение страницы
show_boats_page(st.session_state.get('school_name', None))
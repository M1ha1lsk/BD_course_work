import psycopg2
import psycopg2.extras
import streamlit as st
from repositories.boats import get_boats
from repositories.boats import start_boat_explotation
from repositories.school import get_school_role
from repositories.redis_repository import RedisRepository
import json
redis_repo = RedisRepository()
from datetime import date
from settings import DB_CONFIG
import time


def show_selling_boats_page(school_name: str):
    st.title("Покупка лодок")

    if school_name is None:
        st.error("Вы не авторизовались.")
        return
    
    school_role = get_school_role(school_name)
    if not school_role:
        return

    boats = get_boats()
    boat_options = {f"{boat['firm_name']}   {boat['class']}   {boat['user_weight']}": boat['boat_id'] for boat in boats}

    if school_role == "admin":
        query_schools = "SELECT school_name FROM sport_schools;"
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(query_schools)
                schools = cur.fetchall()
        school_names = [school[0] for school in schools]
    else:
        school_names = [school_name]
    
    if school_role == "admin":
        st.subheader("Последние уведомления")
        
        # Создаем контейнер для уведомлений
        notifications_placeholder = st.empty()
        
        # Подписываемся на канал
        pubsub = redis_repo.subscribe_to_channel('new_purchases')
        
        # Проверяем новые сообщения
        message = pubsub.get_message()
        if message and message['type'] == 'message':
            data = json.loads(message['data'])
            notifications_placeholder.info(
                f"Новая покупка: Школа ID {data['school_id']} купила лодку ID {data['boat_id']}"
            )

    selected_boat_name = st.selectbox("Выберите лодку", list(boat_options.keys()))
    school_name = st.selectbox("Выберите школу", school_names)
    deal_date = st.date_input("Выберите дату сделки", min_value=date.today())

    if st.button("Зарегистрировать сделку и начать эксплуатацию"):
        boat_id = boat_options[selected_boat_name]
        
        # Проверяем, не куплена ли лодка уже
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT purchased FROM boats WHERE boat_id = %s", (boat_id,))
                result = cur.fetchone()
                if result and result[0]:
                    st.error("Эта лодка уже куплена!")
                    return
        
        try:
            end_date = start_boat_explotation(boat_id, school_name, deal_date)
            query_update = """
            UPDATE boats SET purchased = TRUE WHERE boat_id = %s;
            """
            with psycopg2.connect(**DB_CONFIG) as conn:
                with conn.cursor() as cur:
                    cur.execute(query_update, (boat_id,))
                    conn.commit()
            
            st.success(f"Эксплуатация лодки {boat_id} началась с {deal_date}. Конец эксплуатации: {end_date}")
            time.sleep(2)
            st.rerun()
        except Exception as e:
            st.error(f"Ошибка: {str(e)}")

show_selling_boats_page(st.session_state.get('school_name', None))


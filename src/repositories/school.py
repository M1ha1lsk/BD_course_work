import psycopg2
import psycopg2.extras
import streamlit as st
from datetime import date
from settings import DB_CONFIG

def get_school_id_by_name(school_name: str) -> int:
    query = """
    SELECT school_id FROM sport_schools WHERE school_name = %s;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (school_name,))
            result = cur.fetchone()
            if result:
                return result[0]
            else:
                st.error(f"Школа с названием '{school_name}' не найдена.")
                return None
            

def get_school_role(school_name: str) -> str:
    query = """
    SELECT school_role FROM sport_schools WHERE school_name = %s;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (school_name,))
            result = cur.fetchone()
            if result:
                return result[0]  # возвращаем роль пользователя
            else:
                st.error(f"Школа с именем '{school_name}' не найдена.")
                return None
            
def get_school_name_by_id(school_id: int) -> str:
    query = "SELECT school_name FROM sport_schools WHERE school_id = %s;"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (school_id,))
            result = cur.fetchone()
            return result[0] if result else "Неизвестная школа"
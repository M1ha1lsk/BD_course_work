import psycopg2
import psycopg2.extras
from repositories.school import get_school_id_by_name
from datetime import date
from settings import DB_CONFIG


def get_boats() -> list[dict]:
    print("Получение лодок")
    query = """
        SELECT b.boat_id, c.firm_name, a.class, a.user_weight 
        FROM boat_specifications as a 
        JOIN boats as b USING(spec_id) 
        JOIN boat_firms as c USING(firm_id)
        WHERE b.purchased != TRUE
        ORDER BY c.firm_name;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            return cur.fetchall()


def start_boat_explotation(boat_id: int, school_name: str, begin_date: date):
    school_id = get_school_id_by_name(school_name)
    if not school_id:
        return  # Если не нашли school_id, прекращаем выполнение

    # Получаем firm_id лодки
    query_firm = """
    SELECT firm_id FROM boats WHERE boat_id = %s;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query_firm, (boat_id,))
            firm_id = cur.fetchone()[0]
    
    # Рассчитываем дату конца эксплуатации на основе firm_id
    if firm_id in [1, 2]:
        end_date = begin_date.replace(year=begin_date.year + 25)  # +25 лет
    elif firm_id == 4:
        end_date = begin_date.replace(year=begin_date.year + 15)  # +15 лет
    elif firm_id in [3, 5, 6]:
        end_date = begin_date.replace(year=begin_date.year + 10)  # +10 лет
    else:
        # Если firm_id не совпадает с ни одним из вышеуказанных, можно поставить стандартную дату конца эксплуатации
        end_date = begin_date.replace(year=begin_date.year + 25)  # по умолчанию +25 лет

    # Запрос для вставки записи в таблицу boat_exploitation с датой начала и конца эксплуатации
    query = """
    INSERT INTO boat_explotation (school_id, boat_id, begin_date, end_date) 
    VALUES (%s, %s, %s, %s);
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (school_id, boat_id, begin_date, end_date))
            conn.commit()

    # Возвращаем успешный результат
    return end_date

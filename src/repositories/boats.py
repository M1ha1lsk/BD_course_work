import psycopg2
import psycopg2.extras
from repositories.school import get_school_id_by_name
from repositories.redis_repository import RedisRepository
import json
redis_repo = RedisRepository()
from settings import DB_CONFIG
from datetime import date, datetime


def get_boats() -> list[dict]:
    # Проверяем кэш
    cached = redis_repo.get_cached_boats_data("available_boats")
    if cached:
        return json.loads(cached)
    
    print("Получение лодок из БД")
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
            result = cur.fetchall()
    
    # Кэшируем результат
    redis_repo.cache_boats_data("available_boats", json.dumps(result))
    return result

def get_firm_name_by_boat(boat_id: int):
    
    query = """
        SELECT firm_name
        FROM boat_firms
        WHERE firm_id = (SELECT firm_id FROM boats WHERE boat_id = %s);
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (boat_id,))
            result = cur.fetchone()[0]
    
    return result

def start_boat_explotation(boat_id: int, school_name: str, begin_date: date):
    school_id = get_school_id_by_name(school_name)
    if not school_id:
        return None

    # Проверяем, не куплена ли лодка
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT purchased FROM boats WHERE boat_id = %s", (boat_id,))
            if cur.fetchone()[0]:
                raise Exception("Лодка уже куплена")
            
    # Получаем firm_id лодки
    query_firm = """
    SELECT firm_id FROM boats WHERE boat_id = %s;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query_firm, (boat_id,))
            firm_id = cur.fetchone()[0]
    
    # Рассчитываем дату конца эксплуатации
    if firm_id in [1, 2]:
        end_date = begin_date.replace(year=begin_date.year + 25)
    elif firm_id == 4:
        end_date = begin_date.replace(year=begin_date.year + 15)
    elif firm_id in [3, 5, 6]:
        end_date = begin_date.replace(year=begin_date.year + 10)
    else:
        end_date = begin_date.replace(year=begin_date.year + 25)

    # Вставляем запись
    query = """
    INSERT INTO boat_explotation (school_id, boat_id, begin_date, end_date) 
    VALUES (%s, %s, %s, %s);
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (school_id, boat_id, begin_date, end_date))
            conn.commit()
    
    # Отправляем уведомление о новой покупке
    notification = {
        'school_id': school_id,
        'school_name': school_name,  # Добавим имя школы для наглядности
        'boat_id': boat_id,
        'firm_name': get_firm_name_by_boat(boat_id),  # Нужно реализовать эту функцию
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    redis_repo.publish_notification('new_purchases', json.dumps(notification))

    redis_repo.redis.delete("available_boats")    
    
    return end_date
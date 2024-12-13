import psycopg2
import psycopg2.extras
from settings import DB_CONFIG

# Получение ID региона по имени
def get_region_id(region_name):
    query = "SELECT region_id FROM regions WHERE region_name = %s;"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (region_name,))
            result = cur.fetchone()
            return result[0] if result else None

# Получение всех регионов из базы
def get_all_regions():
    query = "SELECT region_name FROM regions;"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            regions = [row[0] for row in cur.fetchall()]
    return regions
import psycopg2

conn_params = {
    "host": "localhost",
    "database": "vacancies",
    "user": "postgres",
    "password": "07052001",
}

with psycopg2.connect(**conn_params) as conn:
    with conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS vacancies;")
        conn.commit()

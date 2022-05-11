import psycopg2
import yaml


with open('host.yml') as config_file:
    config = yaml.load(config_file, Loader=yaml.FullLoader)

connection = psycopg2.connect(
    host=config['host'],
    user=config['user'],
    password=config['password'],
    database=config['database']
)
connection.autocommit = True


def create_tables():
    data_sources = ["binance_data", "central_bank_data"]
    for i in data_sources:
        with connection.cursor() as cursor:
            cursor.execute(f"""
                           CREATE TABLE {i}(
                           id SERIAL PRIMARY KEY,
                           time_received VARCHAR(26),
                           price NUMERIC)""")


if __name__ == '__main__':
    create_tables()

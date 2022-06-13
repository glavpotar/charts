from yoyo import step


apply_sql = """
        CREATE TABLE binance_exchange_rates(
            id SERIAL PRIMARY KEY,
            datetime TIMESTAMP,
            timestamp BIGINT,
            binance_btc_usdt NUMERIC,
            binance_btc_rub NUMERIC,
            binance_usdt_rub NUMERIC);
        
        CREATE TABLE cbrf_exchange_rates(
            id SERIAL PRIMARY KEY,
            datetime TIMESTAMP,
            timestamp BIGINT,
            cbrf_usdt_rub NUMERIC);
            
        CREATE TABLE actions(
            id SERIAL PRIMARY KEY,
            datetime TIMESTAMP,
            timestamp BIGINT,
            base VARCHAR,
            quote VARCHAR,
            bought_at DOUBLE PRECISION,
            quantity INTEGER);
            
        CREATE TABLE sessions(
            id SERIAL PRIMARY KEY,
            keyword VARCHAR,
            password VARCHAR);
            
        CREATE TABLE pushy_users(
            id SERIAL PRIMARY KEY,
            device_token VARCHAR);
        """


def apply_step(conn):
    with conn.cursor() as cursor:
        cursor.execute(apply_sql)


steps = [step(apply_step)]

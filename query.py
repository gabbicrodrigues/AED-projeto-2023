import psycopg2

# Função para realizar consultas nas tabelas
def perform_queries(database, user, password, host):
    try:
        conn = psycopg2.connect(
            dbname=database,
            user=user,
            password=password,
            host=host
        )
        cursor = conn.cursor()

        # Consultas de exemplo
        cursor.execute("SELECT * FROM sua_tabela")
        rows = cursor.fetchall()

        print(f"Dados de {database}:")
        for row in rows:
            print(row)

        conn.close()

    except psycopg2.Error as e:
        print(f"Erro de conexão ou consulta: {e}")

# Realizar consultas nas bases de dados
def query_databases():
    databases = {
        "db1": {"user": "user1", "password": "pass1", "host": "postgres-db1"},
        "db2": {"user": "user2", "password": "pass2", "host": "postgres-db2"},
        "db3": {"user": "user3", "password": "pass3", "host": "postgres-db3"}
    }

    for db_name, config in databases.items():
        perform_queries(db_name, config["user"], config["password"], config["host"])

query_databases()
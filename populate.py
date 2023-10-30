import psycopg2

# Função para preencher as tabelas com dados
def populate_data(database, user, password, host):
    try:
        conn = psycopg2.connect(
            dbname=database,
            user=user,
            password=password,
            host=host
        )
        cursor = conn.cursor()

        # Defina a lógica para gerar dados e executar as inserções em massa aqui
        # Abaixo está um exemplo simples de inserção em uma tabela fictícia

        # Crie uma tabela (se ela não existir)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sua_tabela (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100),
                email VARCHAR(100)
            )
        """)

        # Gere dados de exemplo e insira-os na tabela
        for i in range(1, 10000):  # Insira 10.000 linhas
            cursor.execute(f"INSERT INTO sua_tabela (nome, email) VALUES ('Nome{i}', 'email{i}@exemplo.com')")

        # Salve as alterações e feche a conexão
        conn.commit()
        conn.close()
        print('dados inseridos com sucesso!')

    except psycopg2.Error as e:
        print(f"Erro de conexão ou inserção: {e}")

# Acessar e popular os bancos de dados
def populate_databases():
    databases = {
        "db1": {"user": "user1", "password": "pass1", "host": "postgres-db1"},
        "db2": {"user": "user2", "password": "pass2", "host": "postgres-db2"},
        "db3": {"user": "user3", "password": "pass3", "host": "postgres-db3"}
    }

    for db_name, config in databases.items():
        populate_data(db_name, config["user"], config["password"], config["host"])


FROM python:3.9

WORKDIR /app

RUN apt-get install libpq-dev

RUN pip install psycopg2

# Copia o script Python para o contêiner
COPY app.py populate.py query.py  /app/

# Comando para rodar a aplicação
CMD ["python", "/app/app.py"]

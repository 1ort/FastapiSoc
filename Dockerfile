FROM python:3.10

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
EXPOSE 80

# Do not use in production! To generate a secret use:
# openssl rand -hex 32
ENV SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7 

ENV ACCESS_TOKEN_EXPIRE_MINUTES=30

ENV DATABASE_URL=sqlite:////app/app.db

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
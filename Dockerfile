FROM python:3.10

RUN mkdir /simplesocial
COPY /simplesocial /simplesocial
COPY pyproject.toml /simplesocial

WORKDIR /simplesocial
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

EXPOSE 80

# Do not use in production! To generate a secret use:
# openssl rand -hex 32
ENV SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7 
ENV ACCESS_TOKEN_EXPIRE_MINUTES=30
ENV DATABASE_URL=sqlite:////simplesocial/app.db

CMD ["uvicorn", "simplesocial.main:app", "--host", "0.0.0.0", "--port", "80"]
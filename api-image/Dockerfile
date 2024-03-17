FROM python:3.10.12
WORKDIR /usr/src/app
COPY main.py /usr/src/app/
RUN pip install fastapi[all]
CMD ["uvicorn", "main:app", "--port", "8000", "--host", "0.0.0.0"]
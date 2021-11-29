FROM python:3.8
COPY ./requirements.txt .
RUN pip install -r requirements.txt
CMD ["uvicorn", "app.main:app", "--port", "80", "--host", "0.0.0.0"]
FROM python:3.8.3-slim-buster
RUN python -m pip install --upgrade pip
WORKDIR /app
COPY . .
RUN pip install PyMySQL
RUN pip install -r requirements.txt
RUN pip install --upgrade 'SQLAlchemy<1.4'
CMD ["python", "app.py"]
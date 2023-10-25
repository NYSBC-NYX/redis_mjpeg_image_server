FROM python:latest
WORKDIR /app
COPY ./requirements.txt /app
COPY ./wsgi.py /app
RUN pip install -r requirements.txt
COPY . .
EXPOSE 3908
ENV FLASK_APP=flask_streamer.py
CMD ["uwsgi", "--socket", ":3909", "--protocol", "http", "--master", "-p", "5", "-w", "wsgi:app"]

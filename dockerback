FROM python:3.10.6

EXPOSE 80

EXPOSE 35/udp

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "-u", "bot.py"]
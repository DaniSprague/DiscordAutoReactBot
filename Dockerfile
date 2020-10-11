FROM python:3.8-alpine
WORKDIR /usr/src/autoreact
COPY bot.py .
RUN apk add build-base
RUN pip install discord.py
RUN pip install python-dotenv
RUN pip install emoji
CMD ["python3", "bot.py"]
FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" > /etc/apk/repositories \
    && echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories \
    && echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories \
    && echo "http://dl-cdn.alpinelinux.org/alpine/v3.11/main" >> /etc/apk/repositories \
    && apk upgrade -U -a \
    && apk add --no-cache \
    gcc \
    linux-headers \
    libstdc++ \
    chromium \
    freetype \
    ttf-freefont \
    chromium-chromedriver \
    && rm -rf /var/cache/* \
    && mkdir /var/cache/apk
EXPOSE 5000
COPY . .
ENV DISPLAY=:99
CMD ["python", "-m", "flask", "run"]

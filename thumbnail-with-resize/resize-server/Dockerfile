FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apk update
RUN apk add --no-cache imagemagick bash pngcrush optipng=0.7.7-r0
EXPOSE 4000
COPY . .
CMD ["python", "app.py"]

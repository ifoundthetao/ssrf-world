FROM python:3.7-alpine
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apk update
RUN apk add --no-cache imagemagick bash pngcrush optipng=0.7.7-r0
COPY . .
CMD ["python", "app.py"]

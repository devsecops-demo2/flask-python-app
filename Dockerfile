FROM python:3.8

WORKDIR /app
COPY ./app /app/
RUN pip3 install -r requirements.txt
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

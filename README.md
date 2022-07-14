# flask-python-app

## Pre-requisites
```
Docker
Docker-compose
Git
```
### Clone the repository
```
git clone https://github.com/rajshivage/flask-python-app.git

cd flask-python-app
```
### create .env file and add database password
```
echo DB_PASSWORD=<Database Password> > .env
```
### Run docker-compose
```
docker-compose up
```
### Test
```
curl http://127.0.0.1:5000/initdb
curl http://127.0.0.1:5000/widgets
curl http://127.0.0.1:5000/about/
```

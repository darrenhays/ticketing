# Assumptions
- That you know your ass from a hole in the ground
- You are using a Linux terminal with bash
# Setup
### Bash Profile
- Add the following to bash profile
```
export PYTHONUNBUFFERED=1
export FLASK_DEBUG=1
```
- Source bash profile

### Virtual Environment
- Create a virtual environment for the project
```
mkvirtualenv -p python3 ticketing
```

- Install environment requirements from file
```
pip install -r requirements.txt
```

### Redis
- Create a docker container for redis
```
docker run --name redis -d -p 6379:6379 redis
```
- NOTE: Once the container is created you may start the container using the following
```
docker start redis
```
# Testing
- Run flask
```
flask run
```
- In a separate terminal
```
python -m pytest
```
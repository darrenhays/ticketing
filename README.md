# Assumptions
- You are using a Linux terminal with bash installed
# Setup
### Virtual Environment
```
# Install virtual environment wrapper
pip install virtualenvwrapper

# Create a virtual environment for the project
mkvirtualenv -p python3 ticketing

# Activate virtual environment
workon ticketing

# Install environment requirements from file
pip install -r requirements.txt
```
### Redis
```
# Create a docker container for redis
docker run --name redis -d -p 6379:6379 redis
```
###### NOTE: Once the container is created you may start the container using the following
```
docker start redis
```
### Flask
```
# Run flask
flask run
```

# Testing
### Flask Setup
```
# Set the following options in your terminal
export PYTHONUNBUFFERED=1
export FLASK_DEBUG=1

# Run flask
flask run

# In a separate terminal run the tests
python -m pytest
```
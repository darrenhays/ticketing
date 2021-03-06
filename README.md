# Assumptions
- You are using a Linux based Bash
- You are using Python 3.6 for ```python3```
  - Verify with ```python3 --version```  
# Setup
### Virtual Environment
```
# Install virtual environment
pip install virtualenv

# Install virtual environment wrapper
pip install virtualenvwrapper

# Create a virtual environment for the project
mkvirtualenv -p python3 ticketing

# Activate virtual environment
workon ticketing
```
### Install requirements
```
# Install environment requirements from file
pip install -r requirements.txt
```
### Configure AWS
- Request AWS access from an admin
```
aws configure
# Provide access key ID, secret access key, and region (us-est-2)

```
### Flask
```
# Set the following options in your terminal
export PYTHONUNBUFFERED=1
export FLASK_DEBUG=1

# Run flask
flask run
```
- Flask can be accessed @ http://localhost:5000

# Testing
```
# Run flask
flask run

# In a separate terminal run the tests
python -m pytest
```
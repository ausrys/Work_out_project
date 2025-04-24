# 📈 Work out app

This is a simple workout app where an user can register and get work out programs based on his level of experience, age.

- Register
- Get work out plans.

The app uses the `django` web framework for API's and 'postgres' DB for storing user information and workout plans.

--

## 🚀 Features

- Register as a user
- Create plans based on the user information
- Create expertiese levels
- JSON-based RESTful API
- Saves a stock info to the database for later use
- Ability to find records based on attributes

## 📦 Installation


### With out docker:

- Clone the repository
- Inside the stocl_api folder run:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
- Install dependencies
```
pip install -r requirements.txt
```

Run the program:
```
python manage.py runserver
```

### With docker:

```
docker-composer build
docker-comperer up
```


## API ENDPOINTS

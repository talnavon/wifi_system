Verify that pip of python 3.6 is installed, you can verify with "pip -V"
Run pip install -r requirements.txt
Download and install Postgres from: https://www.enterprisedb.com/software-downloads-postgres
Once you have a working Postgres server on your system, open the Postgres interactive shell "psql" and create the database:
# CREATE DATABASE wifi_network_drf;

To run tests: python3 manage.py test
To start server: python3 manage.py runserver

After server started: go to http://127.0.0.1:8000/
Through the swagger UI you can send a GET request only
The POST and PUT request can be send through POSTMAN for example.

https://realpython.com/test-driven-development-of-a-django-restful-api/#django-app-and-rest-framework-setup

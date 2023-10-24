## instructions to start project ##

1. `docker-compose build`
2. `docker-compose run web python3 manage.py makemigrations`
3. `docker-compose run web python3 manage.py migrate`

## create a user to access the admin site
4. `docker-compose run web python3 manage.py createsuperuser`

## this step is to fill the postgres with data from sqlite
5. `docker-compose run web python3 db_parser/load_data.py`

## this step to start the project
6. `docker-compose up` || `docker-compose start`

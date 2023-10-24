## instructions to start project ##

1. docker-compose build
2. docker-compose run web python3 manage.py makemigrations
3. docker-compose run web python3 manage.py migrate
4. docker-compose run web python3 db_parser/load_data.py
5. docker-compose up or docker-compose start

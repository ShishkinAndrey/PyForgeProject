# PyForge
## To run project locally:
```shell
docker-compose up -d --build
```
## To run tests:
```shell
docker-compose run --entrypoint /src/web_app/entrypoint_test.sh --rm web pytest 
```
Flask app will be available at the localhost:
 - `http://localhost:5000/`

## To run project in production:
```shell
docker-compose -f docker-compose.prod.yml up -d --build
```
## If you run project first time you need to run next commands:
- `docker-compose -f docker-compose.prod.yml exec web python manage.py create_db` - to create tables in database
- `docker-compose -f docker-compose.prod.yml exec web python manage.py add_roles` - to add user's roles
- `docker-compose -f docker-compose.prod.yml exec web python manage.py add_data` - add initial data

Flask app will be available at the localhost:
 - `http://localhost:1337/`
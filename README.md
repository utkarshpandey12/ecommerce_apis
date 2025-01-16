# Ecommerce APIs

## Local Development

- Create & activate virtual environment

    - Read the below link to create and activate virtual environments as per your platform.
    - https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/

### Run the Stack

- git clone
- cd repo_base
- activate virtual environemnt ex mac os::

    python3 -m venv .venv
    source .venv/bin/activate

-   Install requirements

    (.venv) pip install -r requirements.txt

-   Build Docker 
    
    (.venv) docker compose -f docker-compose.yml build

-   Apply migrations to postgres DB

    (.venv) docker compose exec web python manage.py migrate

-   Start webserver 

    (.venv) docker compose -f docker-compose.yml up


    

### Running Migrations

- To run **makemigrations**, use this command:

    (.venv) $ docker compose exec web python manage.py makemigrations

- To run **migrate**, use this command:

    (.venv)  $ docker compose exec web python manage.py migrate


### Service Links & Ports

- Django Admin Page Available on:

      http://127.0.0.1:8000/admin/

- API Documentation:

      http://127.0.0.1:8000/api/schema/swagger-ui/


### Folder Structure

- Detail Folder Structure:

        .
        └──ecomm/
            ├── ecommerce_api - (all app urls live here)/
            │   ├── urls.py   -> starting point of routes
            │   ├── settings.py   base settings
            ├── api/
            │   │   ├── models.py -> product and order models
            │   │   ├── views.py -> product and order api views
            │   │   └── urls.py -> product and order api urls
            │   └   |── serializers.py -> api validations
            |   |   |__ exceptions.py -> exceptions definitions
            |   |   |__ dataclasses.py -> api body objects validation definitions
            ├── requirements.txt
            └── manage.py





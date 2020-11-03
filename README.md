# API Goods

REST API for Goods service

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

First install and activate virtual environment in your local project:

```
python3 -m venv venv
. venv/bin/activate
```

### Installing

Install dependencies:

```
python -m pip install -r requirements.txt
```

Migrate database:

```
python manage.py migrate
```

Create superuser with command:

```
python manage.py createsuperuser
```
Run server:

```
python manage.py runserver
```
## Deployment

Run application in docker container:

```
docker-compose up
```
## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
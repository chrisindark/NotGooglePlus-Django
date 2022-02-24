# Environment

Prerequisites:

- Python 3.8

Checkout the repo:

```bash
git clone https://xxx@xxx/xxx/xxx.git
```

Install pipenv

```bash
pip install pipenv
```

Create virtualenv:

```bash
# virtualenv env
# source env/bin/activate
pipenv install
pipenv shell
```

Install requirements:

```bash
# pip install -r requirements.txt
```

Migrate the database:

```bash
python manage.py migrate
```

Create a superuser:

```bash
python manage.py createsuperuser
```

Collect static files from each of your applications into a single location:

```bash
python manage.py collectstatic
```

Start the development http server

```bash
python manage.py runserver --settings=notgoogleplus.settings.development
```

Open your web browser and go to `127.0.0.1:8000/`

Start the development daphne server for websocket interface server

```bash
daphne -b 127.0.0.1 -p 8001 notgoogleplus.asgi:channel_layer
```

Start the worker servers to process websocket requests

```bash
python manage.py runworker --settings=notgoogleplus.settings.development
```

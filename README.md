# Environment #

Prerequisites:

* Python 2.7

Checkout the repo:
```bash
git clone https://xxx@xxx/xxx/xxx.git
```

Create virtualenv:
```bash
virtualenv env
source env/bin/activate
```

Install requirements:
```bash
pip install -r requirements.txt
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

Start the development server
```bash
python manage.py runserver
```

Open your web browser and go to `localhost:8000/`
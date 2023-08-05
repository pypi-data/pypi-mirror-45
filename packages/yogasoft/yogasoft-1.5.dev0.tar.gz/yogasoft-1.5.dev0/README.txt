0) Create environment
   sudo apt-get install python3-dev xephyr xvfb
   python3 -m venv env36
   source env36/bin/activate
   pip install -r requirements/dev.txt

1) Run tests
   source env36/bin/activate
   docker-compose up    # start databases
   python manage.py test


start  daphne server for channels, it runs on 8002
source env36/bin/activate
python manage.py makemigrations
python manage.py migrate

python manage.py collectstatic

daphne -b 0.0.0.0 -p 8002 yogasoft.asgi:channel_layer
python manage.py runserver 0.0.0.0:8000


3) MANIFEST.in is used for package release

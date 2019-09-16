# Thai Ingredients Detector

[![Python Version](https://img.shields.io/badge/python-3.7-brightgreen.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-2.1-brightgreen.svg)](https://djangoproject.com)

## How Running the Project

Clone the repository to your local machine:

```bash
https://github.com/TrinVeerasiri/thaiingdetector.git
```

***The model (model.pt) is a large file and must download separately.
You can download on GitHub at "thaiingdetector/model.pt" (337 MB). 
At local, put "model.pt" in "thaiingdetector-master" directory.***

Install the requirements:

```bash
pip install -r requirements.txt
```

Apply the migrations:

```bash
python manage.py migrate
```

Run the development server:

```bash
python manage.py runserver
```

The project available at **127.0.0.1:8000**

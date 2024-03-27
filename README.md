# Blogicum

Create your own blog with ease.

## Description

Blogicum is a Django project which represents a multi-page blogging website that allows you to manage your publications through a connected relational database.

## Getting Started

### List of used technologies

* `Python`
* `Django ORM`
* `SQLite`
* `HTML`
* `CSS`

### Dependencies

You can find all used packages in `requirements.txt` file.

### Installation

Use the following commands in your terminal to prepare your project for local lauch and modification.

* Creating local copy of the project
```
git clone https://github.com/ArtemMaksimov-trial/django_sprint4.git
```
* Creating virtual environment from the root folder `.../django_sprint4`
```
python -m venv venv
```
* Activating a virtual environment
```
source venv/Scripts/activate
```
* Setting up of the required dependencies
```
pip install -r requirements.txt
```
* Switching to an internal folder `.../django_sprint4/blogicum`
```
cd blogicum
```
* Applying of necessary migrations
```
python manage.py migrate
```
* Creating superuser
```
python manage.py createsuperuser
```
* Running of the local server
```
python manage.py runserver
```

Now you can go to the local address `http://127.0.0.1:8000/` in your browser to see website at work.

To get access to admin interface go to `http://127.0.0.1:8000/admin/` and enter username and password of superuser that you created.

That's it! Now you are ready to manage and modify website application for your purposes.

## Contact

Artem Maksimov - [@ovienrait](https://t.me/ovienrait) - [nirendsound@gmail.com](https://nirendsound@gmail.com)

Project Link: [https://github.com/ArtemMaksimov-trial/django_sprint4.git](https://github.com/ArtemMaksimov-trial/django_sprint4.git)

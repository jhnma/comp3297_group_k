# COMP3297 Group K HotZone

## Setup
Create a .env file in the `hotzone_project` folder with the following content:
```
DATABASE_URL='postgres://db_user:db_password@db_hostname:5432/db_name'
HOTZONE_SECRET_KEY='r@ubiaqsdy*q%%$3$ip7_e(gcenq!^g5bv)0%tgm@pylivmiy%'
HOTZONE_DEBUG=True
```
Replace db_user, db_password, db_hostname, db_name with the values for your local database\
Change the port too if your database is not running on 5432

---
## For Local Test:
Windows with waitress (default runs on port 8080)
```
heroku local -f Procfile.waitress
```
Other OS with gunicorn
```
heroku local
```
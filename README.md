# VirtualDoctor

### Setup instructions
1.     git clone https://github.com/jonathanhanley/VirtualDoctor.git
2.     cd VirtualDoctor
3.     python3 -m venv venv
4.     source venv/bin/active
5.     pip install -r requirements.txt
6.     python manage.py test
7.     python manage.py runserver

### Credentials - Local only.
| Account Type        | Username           | Password           |
| ------------- |:-------------:| :-------------:| 
| Admin    | admin | admin |
| User    | testemail@gmail.com | MyTestPassword123 |


### Urls
| Page        | Url           |
| ------------- |:-------------:| 
| Authentication Documentation (local)     | [Postman](https://documenter.getpostman.com/view/11213399/UV5c9v2K) | 


### TODO
1. ~~Create Django Project~~
2. ~~Setup DRF~~
3. ~~Authentication API~~:
    1. ~~Register~~
    2. ~~Login~~
    3. ~~Delete Account~~
    4. ~~Get User details~~
    5. ~~Logout~~
    
4. Dockerized project
    
5. Questions DB:
    1. Create question
    2. Create sub question
    3. Get Question
    4. Get Sub question
    5. Save Question
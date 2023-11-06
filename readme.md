## 3DBlog
![](./screen_shot.png)

### 1. Init project
###### Automatic config

execute this command with make to config automatic env 
> make init

###### Manuel config

create local env
> python3 -m venv env

connect to local env
> source env/bin/activate

install project dependencies
> pip install -r requirements.txt

### 2. Execute project
###### By Docker

> docker-compose up


###### By Flask Server
> flask run

### 3. Endpoints

| Actions        | Endpoints                             | Method |
|----------------|---------------------------------------|--------|
| Create Users   | localhost:3000/api/v1/users           | **POST**   |
| Update Users   | localhost:3000/api/v1/users/{user_id} | **PUT**    |
| Get User       | localhost:3000/api/v1/users/{user_id} | **GET**    |
| Paginate Users | localhost:                            | **GET**    |

NB: for more detail click localhost:3000/docs# from docker container

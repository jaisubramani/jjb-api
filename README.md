# jjb-api


## To start services 

`docker-compose up --build`


## To interact with rest api endpoints

`curl http://localhost:8000/v1/version`

`curl http://localhost:8000/v1/job -X PUT -H 'content-type: application/json' -d '{"project": "all"}'`

`curl http://localhost:8000/v1/job -X POST -H 'content-type: application/json' -d '{"project": "php-app", "type": "docker"}'`

`curl http://localhost:8000/v1/job -X DELETE -H 'content-type: application/json' -d '{"project": "php-app", "type": "docker"}'`

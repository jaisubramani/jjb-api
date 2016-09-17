# jjb-api

## Start services

`docker-compose up --build`

## Change Jenkins password

login to `http://localhost:8080` and change `admin` user password to `admin`

## Check if jjb service is up

`curl http://localhost:8000/v1/version`

## Update all jobs

`curl http://localhost:8000/v1/job -X PUT -H 'content-type: application/json' -d '{"project": "all"}'`

## Create jobs

`curl http://localhost:8000/v1/job -X POST -H 'content-type: application/json' -d '{"project": "php-app", "type": "docker"}'`

## Delete jobs

`curl http://localhost:8000/v1/job -X DELETE -H 'content-type: application/json' -d '{"project": "php-app", "type": "docker"}'`

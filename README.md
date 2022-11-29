# Store user statistics

## Description

Backend part of web application based on REST API.
The solution that could be used by online stores as an additional place to collect statistics on user activity on the store/site.
The application will be responsible for processing users' personal data, as well as collecting and analyzing the data provided by store about those users while using the online store.

## Features
- Project for processing user data in microservices
- Microservices store and manage information about user data and events (user activity on the site)
- Microservices interact with each other through REST API
- The project is placed in Docker containers managed with docker-compose
- API for external clients is provided by API Gateway service on port 8000
- User information is confidential and stored in a different place than his statistics (User Personal Info service and Event Info service)
- The solution allows operations on a large number of events
- Using pre-commit hooks

## Technologies

- FastAPI
- Flask
- PostgreSQL
- SQLAlchemy
- Docker

## Prerequisites
- Docker

## Usage
Start the docker containers

> docker-compose up -d --build

OpenAPI documentation (Swagger):
> /docs

or

> /redos

## Endpoints

### API Gateway service (port 8000)
- POST api/auth/
```
request:
{

}

response (code 201):
{

}
```


### User Personal Info service (port 8001)
- GET /api/user/<user_email>
```

response (code 200):
{
    "id": str(uuid)
}
```
- POST /api/user
```
request:
{
    "email": str,
    "username": str,
    "first_name": str,
    "last_name": str,
    "phone": int,
    "store_id": int
}

response (code 201):
{
    "id": str(uuid)
    "email": str,
    "username": str,
    "first_name": str,
    "last_name": str,
    "phone": int,
    "store_id": int
}
```
- PATCH /api/user
```
request:
{
    "email": str,
    "username": str,
    "first_name": str,
    "last_name": str,
    "phone": int,
    "store_id": int
}

response (code 201):
{
    "message": "User successfully updated"
}
```
- DELETE /api/user/<user_id>
```

response (code 200):
{
    "message": "User successfully deleted"
}
```


### Event Info service (port 8002)
- POST /api/event
```
request:
{
  "type": str,
  "store_id": int,
  "user_id": str,
  "data": json
}

response (code 201):
{
  "id": int,
    "type": str,
  "store_id": int,
  "user_id": str,
  "data": json
  "created_at": datetime
}
```

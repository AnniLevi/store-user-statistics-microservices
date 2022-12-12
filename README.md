# Store user statistics

### Description

Backend part of web application based on REST API.
The solution that could be used by online stores as an additional place to collect statistics on user activity on the store/site.
The application will be responsible for processing users' personal data, as well as collecting and analyzing the data provided by store about those users while using the online store.

- Project for processing user data in microservices
- Microservices store and manage information about user data and events (user activity on the site)
- Microservices interact with each other through REST API
- The project is placed in Docker containers managed with docker-compose
- API for an external client is provided by service API Gateway on port 8000
- User information is confidential and stored in a different place than his statistics
- The solution allows operations on a large number of events

### Technologies

- FastAPI
- Flask
- PostgreSQL
- SQLAlchemy
- Docker

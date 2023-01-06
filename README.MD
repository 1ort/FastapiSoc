# simplesocial
Implemented:
- ```username:password``` authentication and registration. All actions require a JWT token in the request headers
- Readonly viewing posts and users is available without authorization
- The functionality of a personal account: Ability to change login details and delete account
![изображение](https://user-images.githubusercontent.com/83316072/211105583-b7cc08f1-8b67-4da7-81c6-ab4f25050dfc.png)
- View other people's profiles and their posts. Ability to get a profile by ID
![изображение](https://user-images.githubusercontent.com/83316072/211105707-e2fa09a9-5759-46fa-bd90-898a83f350dd.png)
- As a user, you can write, edit and delete your own posts. You can like and dislike other people's posts.
![изображение](https://user-images.githubusercontent.com/83316072/211105848-f7535423-66f2-40b0-ade4-09ff6d2420b3.png)

- Each endpoint is documented and contributes to the overall open-api scheme

## Database

The application has been tested and developed with the SQLite database, but since the sqlalchemy is used, you can specify the url for MYSQL, PostgreSQL and other relational databases.


## Installation
It is assumed that you already have git and docker installed.

Clone repo

```git clone https://github.com/1ort/simplesocial.git```

```cd simplesocial```

...and run

```docker compose up```

Ready! The application is running on port 8000.
Online documentation is available at:

```
http://0.0.0.0/8000/docs
http://0.0.0.0/8000/redoc
```

### Important!
Don't use default settings in production.
You need to generate and supply your own private key.

```openssl rand -hex 32```

And then put it in a docker-compose.yml file

```
environment:
      - SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
```

Alternative ways to transfer the private key to the application are here: https://docs.docker.com/compose/environment-variables/


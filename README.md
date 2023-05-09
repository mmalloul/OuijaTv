# Ouija.TV

To be able to run the application locally you have to do the following.

Create the file `docker-compose.override.yml`in the root directory.
This way you override the url to localhost instead

Add the following code to the file.

```
services:
  app:
    environment:
      PUBLIC_WS_URL: ws://localhost:8000

  backend:
    ports:
      - 8000:8000
```

run the command `docker compose up -d`

# Ouija.TV

## Running Application

### Local development

To run the svelte frontend in development:\
`npm i`\
`npm run dev`

To run Python back end:\
`cd python`\
`python server.py`

### Docker

To be able to run the application locally you have to do the following.

Create the file `docker-compose.override.yml` in the root directory.
This way you override the url to localhost instead

Add the following code to the file.

```
services:
  app:
    environment:
      PUBLIC_WS_URL: ws://localhost:8000
      NODE_ENV: dev

  backend:
    ports:
      - 8000:8000

```

run the command `docker compose up -d`

## Deployment

### Staging

**Currently there is no staging environment**

### Production

Deployment to production is implemented in the gitlab ci-cd pipeline when changes are merged to main.

TODO:

- Version control
- Docker security on ports

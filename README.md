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
      PUBLIC_URL: http://localhost:8000
      NODE_ENV: dev

  backend:
    ports:
      - 8000:8000
    environment:
      PUBLIC_API_KEY_OPENAI: <SECRET>
  
  chatbot:
    environment:
      TWITCH_CLIENT_ID: <SECRET>
      TWITCH_REFRESH_TOKEN: <SECRET>
      TWITCH_TOKEN: <SECRET>

```

run the command `docker compose up -d`\

for a fresh build run the command `docker compose up --build -d`

## Deployment
This stage deploys the application to the target environment. It includes two jobs: deploy-production and deploy-staging. These jobs deploy the application to the production and staging environments, respectively.
Each job is configured with specific settings, such as the Docker image used, script commands to execute, and any additional configuration required.

FROM node:18-buster-slim AS base

WORKDIR /opt/app

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential python dumb-init && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["dumb-init", "--"]

FROM base as build

COPY . .

RUN npm install

RUN npm run build

FROM base as deploy

COPY --from=build /opt/app/package.json .
COPY --from=build /opt/app/build .

RUN npm install --omit=dev

CMD ["node", "index.js"]
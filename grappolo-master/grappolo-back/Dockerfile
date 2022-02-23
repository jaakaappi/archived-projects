FROM node:16.13.2 as build
WORKDIR /app
COPY package*.json ./
COPY index.js ./
RUN npm ci --production
CMD node ./index.js
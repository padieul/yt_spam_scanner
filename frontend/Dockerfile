FROM node:12-alpine

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install

RUN npm audit fix

COPY . .

EXPOSE 5000

ENV HOST=0.0.0.0

RUN npm run build

CMD [ "npm", "start" ] 
FROM node:14-alpine

WORKDIR /usr/src/app

COPY vite.config.js ./
COPY package*.json ./

RUN npm install

RUN npm audit fix 

RUN npm update

COPY . .

EXPOSE 5000

ENV HOST=0.0.0.0

RUN npm run build

RUN npm update

CMD ["npm", "run", "dev"]

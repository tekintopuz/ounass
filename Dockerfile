# pull official base image
FROM node:15.8.0-alpine

# set work directory
RUN mkdir -p /var/ounass
RUN mkdir -p /var/ounass/frontend
WORKDIR /var/ounass/frontend

COPY ./package.json .
COPY ./package-lock.json .

RUN npm install -g serve
RUN npm install

# copy react project
COPY . .

RUN npm i
CMD ["npm", "run", "start"]

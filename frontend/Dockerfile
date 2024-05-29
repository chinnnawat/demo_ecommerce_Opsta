FROM node:21.6.2-alpine
WORKDIR /appFront
COPY package.json ./
RUN npm install
COPY . .
RUN npm run build
COPY .next ./.next

EXPOSE 3000
CMD [ "npm", "run", "dev" ]
FROM node:18.20.5-bullseye-slim

RUN npm install -g npm@9.1.3

ADD package.json .
ADD app.js .
ADD order.js .
ADD product.js .
ADD cards.js .
ADD data/cards.json .
ADD data/products.json .
ADD data/orders.json .
COPY . .
RUN npm install

EXPOSE 3030

CMD [ "node", "app.js" ]

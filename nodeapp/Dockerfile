FROM node:18.20.5-bullseye-slim

# Create app directory
WORKDIR /app

# Install app dependencies
COPY package*.json ./
RUN npm install

# Bundle app source
COPY . .

# Expose port
EXPOSE 3000

# Command to run the app
CMD ["node", "app.js"]
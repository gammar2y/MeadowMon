FROM node:18.20.5-bullseye-slim

# Set the working directory
WORKDIR /app

# Install npm globally
RUN npm install -g npm@9.1.3

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Set environment variables
ENV MONGODB_URI=mongodb+srv://meadowmonbusiness:NXVwZOXBQChb01uj@cluster0.mongodb.net/MeadowMon?retryWrites=true&w=majority
ENV REACT_APP_BACKEND_URL=http://localhost:8000

# Expose the port the app runs on
EXPOSE 3000

# Start the app
CMD ["node", "app.js"]
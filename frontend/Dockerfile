# Dockerfile
FROM node:20.16-alpine

WORKDIR /app

# Copy only package files first (for caching)
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci

# Copy the rest of your frontend source
COPY . .

# Build your app (outputs to dist/)
RUN npm run build

# Install serve to serve the production build
RUN npm install -g serve

# Expose port 3000
EXPOSE 3000

# Use serve to serve the `dist` folder
CMD ["serve", "-s", "dist", "-l", "3000"]

# Import builder node image
FROM node:alpine AS builder
# Set workdir
WORKDIR /app
# Copy dependency files to the working directory
COPY package.json package-lock.json ./
# Install dependencies
RUN npm ci
# Copy application code
COPY . .
# Set build environment variables from build arguments
ARG VITE_CLERK_PUBLISHABLE_KEY=""
ENV VITE_CLERK_PUBLISHABLE_KEY=$VITE_CLERK_PUBLISHABLE_KEY
# Build application
RUN npm run build

# Import base caddy image
FROM caddy:2.11-alpine
# Copy the application from the builder
COPY --from=builder /app/dist /app
# Set workdir
WORKDIR /app
# Copy Caddyfile
COPY Caddyfile /etc/caddy/Caddyfile
# Expose ports
EXPOSE 80 443
# Run Caddy
CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile"]
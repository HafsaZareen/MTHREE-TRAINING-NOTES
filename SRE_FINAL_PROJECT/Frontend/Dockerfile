# Stage 1: Build React app
FROM node:18-alpine AS builder

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install --frozen-lockfile
COPY . .
RUN npm run build

# Stage 2: Runtime with Nginx and Exporter
FROM nginx:alpine

# Install nginx-prometheus-exporter
RUN apk add --no-cache curl \
    && curl -L https://github.com/nginxinc/nginx-prometheus-exporter/releases/download/v1.1.0/nginx-prometheus-exporter_1.1.0_linux_amd64.tar.gz -o /tmp/exporter.tar.gz \
    && tar -xzf /tmp/exporter.tar.gz -C /usr/local/bin/ \
    && rm /tmp/exporter.tar.gz

# Copy built frontend files
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose Nginx port and metrics port
EXPOSE 80 9113

# Run Nginx and exporter in parallel
CMD ["sh", "-c", "nginx -g 'daemon off;' & /usr/local/bin/nginx-prometheus-exporter -nginx.scrape-uri=http://localhost:80/stub_status"]
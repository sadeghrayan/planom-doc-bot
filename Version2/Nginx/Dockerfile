# Use the official Nginx image from Docker Hub
FROM nginx:alpine

# Copy the custom Nginx configuration file to the container
#COPY http.conf /etc/nginx/templates/nginx.conf.template
COPY nginx.conf /etc/nginx/templates/default.conf.template

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port 80
EXPOSE 80

# Run the entrypoint script
CMD ["/entrypoint.sh"]

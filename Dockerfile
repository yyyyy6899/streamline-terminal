# Use the official Brave image from LinuxServer
FROM lscr.io/linuxserver/brave:latest

# Set environment variables
ENV PUID=1000 \
    PGID=1000 \
    TZ=Etc/UTC

# Create config folder for persistence (optional at build time)
RUN mkdir -p /config

# Copy custom start script into the container
COPY brave.sh /brave.sh

# Make it executable
RUN chmod 744 /brave.sh

# Expose required ports
EXPOSE 3000 3001

# Run the Brave container using the script
CMD ["/bin/bash", "/brave.sh"]


FROM alpine:latest

# Create a non-root user first
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Install pip
RUN apk update && apk add py3-pip=24.3.1-r0

# Install gcc and other necessary build tools
RUN apk update && apk add gcc=14.2.0-r4 g++=14.2.0-r4

# Install python3-dev and build-essential
RUN apk update && apk add python3-dev=3.12.9-r0
RUN apk update && apk add build-base=0.5-r3
RUN apk update && apk add librdkafka-dev=2.6.1-r0

# Create a virtual environment and activate it
RUN python3 -m venv /adaptor/venv && chown -R appuser:appgroup /adaptor
ENV PATH="/adaptor/venv/bin:$PATH"

# Set the working directory
WORKDIR /adaptor

# Switch to non-root user
USER appuser

# Copy the requirements.txt file into the container
COPY --chown=appuser:appgroup ./requirements.txt /adaptor/

# Install the required Python packages
RUN pip install -r requirements.txt

# Copy the assessment files into the container
COPY --chown=appuser:appgroup ./producer.py /adaptor/
COPY --chown=appuser:appgroup ./utils.py /adaptor/
COPY --chown=appuser:appgroup ./.env /adaptor/
COPY --chown=appuser:appgroup ./telicent_lib /adaptor/telicent_lib

FROM python:3.12-alpine

# Install git and github-cli
RUN apk add --no-cache git github-cli

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Set scripts as executable
RUN chmod +x run_forge.sh run_weekly.sh

# Configure entrypoint to setup git credentials and remote before starting the scheduler
# We use an inline script to setup git dynamically when the container starts using env vars
ENTRYPOINT ["/bin/sh", "-c", "git config --global user.name \"$GIT_USER_NAME\" && git config --global user.email \"$GIT_USER_EMAIL\" && git config --global --add safe.directory /app && (git remote set-url origin https://${GITHUB_TOKEN}@github.com/King-Austin/daily-activity-forge.git || git remote add origin https://${GITHUB_TOKEN}@github.com/King-Austin/daily-activity-forge.git) && python3 scheduler.py"]

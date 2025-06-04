FROM python:3.11-slim-bullseye

# Update and install security patches
RUN apt-get update && \
	apt-get upgrade -y && \
	apt-get install -y --no-install-recommends \
	ca-certificates \
	gnupg \
	curl \
	&& apt-get autoremove -y \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/* \
	&& update-ca-certificates

# Set non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser -d /app appuser

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies as root
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Fix permissions
RUN chown -R appuser:appuser /app

# Collect static files
RUN python manage.py collectstatic --noinput
# Collect static files
RUN python manage.py collectstatic --noinput
RUN python manage.py collectstatic --noinput

# Run gunicorn
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]

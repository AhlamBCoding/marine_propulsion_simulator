# security-hardened container image

# Use specific version for reproducibility
FROM python:3.13.12-slim AS base

# Metadata
LABEL maintainer="ahlambanu.univ@gmail.com"
LABEL description="Marine Propulsion System Simulator - Cloud Security Hardened"
LABEL version="1.0.0"

# Security: Create non-root user
RUN groupadd -r simulator -g 1000 && \
    useradd -r -m -u 1000 -g simulator simulator

# Install only necessary system packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Security: Copy requirements first (layer caching)
COPY src/requirements.txt .

# Security: Install Python packages with verification
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip check

# Copy application code
COPY --chown=simulator:simulator src/ ./src/
COPY --chown=simulator:simulator main.py .
COPY --chown=simulator:simulator demo.py .

# Create directories with proper permissions
RUN mkdir -p /app/data /app/outputs && \
    chown -R simulator:simulator /app/data /app/outputs

# Security: Switch to non-root user
USER simulator

# Security: Set read-only root filesystem (uncomment if app supports)
# Note: SQLite needs write access to data/, so we can't use read-only root
# VOLUME ["/app/data", "/app/outputs"]

# Health check (optional - useful for orchestrators)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Security: Expose only necessary ports (none needed for this CLI app)
# EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/home/simulator/.local/bin:$PATH"

# Default command
CMD ["python", "main.py"]

# Alternative: Run demo
# CMD ["python", "demo.py"]
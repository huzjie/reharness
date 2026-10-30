# reharness reference image (zero runtime dependencies)
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY reharness ./reharness

RUN pip install --no-cache-dir -e .

EXPOSE 8790

ENTRYPOINT ["reharness"]
CMD ["serve", "--port", "8790"]

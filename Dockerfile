FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir requests pycryptodome Flask
CMD ["python", "location_sign.py"]

# # Base image
# FROM python:3.9

# # Set working directory
# WORKDIR /app

# # Install dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy project files
# COPY . .

# # Run the application
# CMD ["python", "app.py"]

# Base image
FROM python:3.9

# Proje dosyalarını çalışma dizinine kopyala
COPY . /app

# Çalışma dizini olarak /app'i belirt
WORKDIR /app

# Gerekli paketleri yükle
RUN pip install -r requirements.txt

# Uygulamayı çalıştır
CMD ["python", "app.py"]
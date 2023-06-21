# Base image olarak Python 3.8 kullanalım
FROM python:3.8

# Çalışma dizinini /app olarak ayarlayalım
WORKDIR /app

# Gerekli paketleri yüklemek için önce requirements.txt dosyasını kopyalayalım
COPY requirements.txt .

# Paketleri yükleyelim
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyalayalım
COPY . .

# Flask uygulamasını çalıştıralım
CMD ["python", "app.py"]

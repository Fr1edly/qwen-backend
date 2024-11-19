# Используем базовый образ с PyTorch
FROM pytorch/pytorch:1.13.0-cuda11.6-cudnn8-runtime

# Устанавливаем зависимости
RUN pip install --no-cache-dir transformers accelerate flask && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Копируем код модели
WORKDIR /app
COPY . /app

# Указываем порт для Flask-сервера
EXPOSE 5000

# Запуск приложения
CMD ["python", "app.py"]

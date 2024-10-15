FROM nvcr.io/nvidia/pytorch:23.01-py3

# Copy project files
COPY . /app
WORKDIR /app

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
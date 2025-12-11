FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt ./
RUN apt-get update \
&& apt-get install -y build-essential git libgl1-mesa-glx libglib2.0-0 --no-install-recommends \
&& pip install --upgrade pip \
&& pip install -r requirements.txt \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*
COPY . .
EXPOSE 8000
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000","--workers","1"]
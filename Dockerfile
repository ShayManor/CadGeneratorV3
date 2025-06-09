FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN curl -L -o /tmp/openscad.tar.xz \
      https://files.openscad.org/openscad-2024.03-x86_64.AppImage && \
    mkdir -p /opt/openscad && \
    tar -xJf /tmp/openscad.tar.xz -C /opt/openscad --strip-components=1 && \
    ln -s /opt/openscad/openscad /usr/bin/openscad && \
    rm /tmp/openscad.tar.xz
COPY . .
ENV PORT=8080
EXPOSE 8080
CMD exec gunicorn --bind :$PORT --workers 2 --threads 8 --timeout 60 app:app
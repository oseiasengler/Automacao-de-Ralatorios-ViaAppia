FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_ROOT_USER_ACTION=ignore

# Dependências de sistema para geopandas / fiona / shapely / pymupdf
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgdal-dev \
        gdal-bin \
        libgeos-dev \
        libproj-dev \
        gcc \
        g++ \
    && rm -rf /var/lib/apt/lists/*

# Usuário não-root
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --no-create-home appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Cria diretório de dados persistentes (sobreposto pelo disco Render em produção)
RUN mkdir -p /data/fotos_inventario && \
    chown -R appuser:appgroup /data /app

USER appuser

EXPOSE 10000

CMD ["uvicorn", "render_api.app:app", "--host", "0.0.0.0", "--port", "10000"]

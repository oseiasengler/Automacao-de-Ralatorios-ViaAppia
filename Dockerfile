FROM python:3.11-slim

# Cria usuário não-root para rodar a aplicação
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --no-create-home appuser

WORKDIR /app

# Instala dependências primeiro (camada cacheável)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Stub de /data para desenvolvimento local sem disco Render montado.
# Em produção o Render monta o disco persistente em /data e sobrepõe esta pasta.
RUN mkdir -p /data/fotos_inventario && \
    chown -R appuser:appgroup /data /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

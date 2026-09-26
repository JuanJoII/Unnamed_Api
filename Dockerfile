FROM python:3.11-slim

# Copiar el binario de uv desde su imagen oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copiar solo los archivos de dependencias primero (aprovecha el caché de Docker)
COPY pyproject.toml uv.lock ./

# Instalar dependencias. 
# --frozen asegura que se respete el uv.lock
# --no-install-project evita instalar tu propio código como paquete aún
RUN uv sync --frozen --no-dev --no-install-project

# Copiar el resto del código fuente
COPY . .

# Sincronizar el proyecto final
RUN uv sync --frozen --no-dev

# Usar 'uv run' para ejecutar uvicorn dentro del entorno virtual que uv gestiona automáticamente
CMD ["uv", "run", "fastapi", "dev", "--host", "0.0.0.0", "--port", "8000"]
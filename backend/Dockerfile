# Usa uma imagem base oficial do Python
FROM python:3.12-alpine

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia o arquivo de dependências (requirements.txt) para o contêiner
COPY requirements.txt /app/

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos do projeto para o diretório de trabalho do contêiner
COPY ./ /app/

# Expõe a porta padrão do Django (8000)
EXPOSE 8000

# Define o comando para iniciar o servidor do Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

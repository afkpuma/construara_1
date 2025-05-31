# Use uma imagem base oficial do Python
FROM python:3.9-slim-buster

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo requirements.txt para o diretório de trabalho
# e instala as dependências. Isso é feito primeiro para aproveitar o cache do Docker.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação para o diretório de trabalho
COPY . .

# Expõe a porta que o Flask vai usar (padrão 5000)
EXPOSE 5000

# Define a variável de ambiente para o Flask
ENV FLASK_APP=app.py

# Permite que o Flask seja acessível de fora do contêiner
ENV FLASK_RUN_HOST=0.0.0.0  

# Comando para rodar a aplicação Flask quando o contêiner iniciar
CMD ["flask", "run"]


# Étape 1 : Image de base Python
FROM python:3.10-slim

# Étape 2 : Répertoire de travail dans le conteneur
WORKDIR /app

# Étape 3 : Variables d’environnement
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Étape 4 : Copier et installer les dépendances
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Étape 5 : Copier tout le code du projet dans le conteneur
COPY . /app/

# Étape 6 : Exposer le port par défaut de Django
EXPOSE 8000

# Étape 7 : Lancer le serveur
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

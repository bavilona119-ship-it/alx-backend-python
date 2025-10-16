# Utiliser l'image Python officielle
FROM python:3.10-slim

# Définir le répertoire de travail à l'intérieur du conteneur
WORKDIR /app

# Empêcher Python de créer des fichiers .pyc
ENV PYTHONDONTWRITEBYTECODE 1

# Empêcher le buffering du stdout/stderr
ENV PYTHONUNBUFFERED 1

# Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt /app/

# Installer les dépendances
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copier tout le code du projet dans le conteneur
COPY . /app/

# Exposer le port 8000 (port Django par défaut)
EXPOSE 8000

# Commande de lancement du serveur Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Test_Backend_Python

## Étapes pour lancer le projet avec Docker
Éxecuter la commande:
```
docker-compose up -d
```

Pour vérifier que les conteneurs sont bien lancés:
```
docker ps
```

Pour vérifier la connexion MySQL
```
mysql -h 127.0.0.1 -P 3306 -u root -p // Entrer le mot de passe (root)

```
L'API est accessible à 127.0.0.1:5000 pour tester

## Étapes pour effectuer les migrations
Avant de tester l'API, il faut quand même effectuer d'abord les migrations.

```
docker exec -it flask_app bash // Accéder au bash du conteneur Flask
flask db migrate -m "Initial migration" // Faire une première migration
flask db upgrade // Appliquer les changements
```
Le dossier migrations existe déjà (créé avec flask db init), donc plus besoin d'éxecuter la commande pour le créer. La table users sera ainsi créé et l'API peut être correctement testé.
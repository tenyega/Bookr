# 📚 Bookr — Documentation Complète Django

> Projet Django de gestion de livres — Master 2 Tableau de Bord — Mars 2026

---

## Table des matières

1. [Qu'est-ce que Django ?](#1-quest-ce-que-django-)
2. [Stack Technique](#2-stack-technique)
3. [Installation et Configuration](#3-installation-et-configuration)
4. [Les Modèles](#4-les-modèles-models)
5. [Les Migrations](#5-les-migrations)
6. [Le Django Shell](#6-le-django-shell)
7. [Les Vues et URLs](#7-les-vues-views-et-urls)
8. [Les Données Créées](#8-les-données-créées)
9. [Mise en ligne sur GitHub](#9-mise-en-ligne-sur-github)
10. [Concepts Clés](#10-concepts-clés-à-retenir)

---

## 1. Qu'est-ce que Django ?

Django est un **framework web Python de haut niveau** qui permet de créer des applications web rapidement et proprement. Il suit le principe **"batteries included"** — tout ce dont vous avez besoin est déjà inclus.

| Concept | Explication |
|---|---|
| **ORM** | Parler à la base de données en Python, sans SQL |
| **Admin Panel** | Interface automatique pour gérer vos données |
| **URL Routing** | Mapper des URLs à des fonctions Python |
| **Templates** | Générer du HTML dynamique |
| **Migrations** | Gérer l'évolution de la structure de la base de données |

### Django vs les alternatives

| | Django | Flask | Streamlit |
|---|---|---|---|
| **Philosophie** | Batteries included | Minimaliste | Data/ML apps |
| **ORM intégré** | ✅ | ❌ | ❌ |
| **Admin panel** | ✅ | ❌ | ❌ |
| **Courbe d'apprentissage** | Modérée | Faible | Très faible |

---

## 2. Stack Technique

| Outil | Version | Rôle |
|---|---|---|
| **Python** | 3.13.9 | Langage de programmation |
| **Django** | 5.x | Framework web |
| **MySQL** | via WAMP | Base de données principale |
| **SQLite** | par défaut | Base de données secondaire |
| **phpMyAdmin** | 5.0.2 | Interface visuelle MySQL |
| **IPython** | 9.7.0 | Shell Django amélioré |
| **WAMP** | 64bit | Serveur local (Apache + MySQL) |
| **GitHub** | — | Versioning et partage du code |

---

## 3. Installation et Configuration

### 3.1 Créer le projet Django

```bash
pip install django
django-admin startproject Bookr
cd Bookr
python manage.py startapp bookOnline
python manage.py startapp backoffice
```

### 3.2 Enregistrer les apps dans settings.py

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    ...
    'bookOnline',   # notre app
    'backoffice',   # notre app
]
```

### 3.3 Configurer les bases de données (settings.py)

Le projet utilise **deux bases de données simultanément** :

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'mysql': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bookr',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

### 3.4 Installer le driver MySQL

```bash
pip install mysqlclient
```

### 3.5 Créer la base de données MySQL

Dans la console MySQL (WAMP) :

```sql
CREATE DATABASE bookr;
SHOW DATABASES;
```

---

## 4. Les Modèles (Models)

Les modèles sont des **classes Python** qui représentent les tables de la base de données. Django les traduit automatiquement en tables SQL via les migrations.

### 4.1 App backoffice — models.py

```python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    code = models.IntegerField()

    def __str__(self):
        return self.name


class ProductItem(models.Model):
    code = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.code
```

### 4.2 App bookOnline — models.py

```python
from django.db import models

class LivreType(models.Model):
    genre = models.CharField(max_length=100)

    class Meta:
        db_table = 'LivreType'

    def __str__(self):
        return self.genre


class LivreStatus(models.Model):
    status = models.CharField(max_length=100)

    class Meta:
        db_table = 'LivreStatus'

    def __str__(self):
        return self.status


class Livre(models.Model):
    nom = models.CharField(max_length=200)
    prix = models.DecimalField(max_digits=6, decimal_places=2)
    type = models.ForeignKey(LivreType, on_delete=models.CASCADE)
    status = models.ForeignKey(LivreStatus, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Livre'

    def __str__(self):
        return self.nom
```

### 4.3 Foreign Keys — Explication

Une **Foreign Key (clé étrangère)** crée un lien entre deux tables :

- `Livre → LivreType` : chaque livre a un genre (roman, polar, etc.)
- `Livre → LivreStatus` : chaque livre a un statut (publié, réimpression, etc.)
- `ProductItem → Product` : chaque item appartient à un produit

> `on_delete=models.CASCADE` signifie que si le parent est supprimé, tous ses enfants le sont aussi.

---

## 5. Les Migrations

Les migrations permettent à Django de **créer et modifier les tables** de la base de données automatiquement à partir des modèles.

```bash
# Générer les fichiers de migration depuis les modèles
python manage.py makemigrations

# Appliquer les migrations à la base de données
python manage.py migrate

# Si les tables existent déjà (créées manuellement)
python manage.py migrate --fake-initial
```

---

## 6. Le Django Shell

Le shell Django est une **console Python interactive** avec tout le projet pré-chargé. Il permet de tester des requêtes, créer des données et déboguer.

```bash
python manage.py shell
```

### 6.1 CRUD de base — Product (SQLite)

```python
# CREATE
p = Product()
p.name = "ipod"
p.code = 1234
p.save()

# Syntaxe courte
Product(name="ipad retina", code=1543).save()

# READ
Product.objects.all()
Product.objects.get(id=1)
Product.objects.filter(name="ipod")
Product.objects.count()

# UPDATE
p = Product.objects.get(id=1)
p.name = "ipod mini"
p.save()

# DELETE
Product.objects.get(id=1).delete()
```

### 6.2 CRUD avec MySQL — Livre

> ⚠️ Toujours ajouter `.using('mysql')` pour cibler la base MySQL

```python
# Créer un type et un status
t, _ = LivreType.objects.using('mysql').get_or_create(genre="roman")
s, _ = LivreStatus.objects.using('mysql').get_or_create(status="toujours publié")

# Créer des livres
Livre(nom="Les Misérables", prix=8, type=t, status=s).save(using='mysql')
Livre(nom="Madame Bovary", prix=7, type=t, status=s).save(using='mysql')
Livre(nom="Honoré de Balzac", prix=11, type=t, status=s).save(using='mysql')

# Lire
Livre.objects.using('mysql').all()
Livre.objects.using('mysql').all().values('id', 'nom', 'prix')
```

### 6.3 Querysets avancés

```python
# Tous les livres
Livre.objects.using('mysql').all()

# Commencent par "L"
Livre.objects.using('mysql').filter(nom__startswith="L")

# Contiennent "Misérables"
Livre.objects.using('mysql').filter(nom__contains="Misérables")

# Prix >= 10
Livre.objects.using('mysql').filter(prix__gte=10)

# Prix >= 10 ET status "toujours publié"
Livre.objects.using('mysql').filter(prix__gte=10, status__status="toujours publié")

# Livre le plus cher
Livre.objects.using('mysql').order_by('-prix').first()
```

### 6.4 Mise à jour des statuts

```python
# Créer nouveaux statuts
s2, _ = LivreStatus.objects.using('mysql').get_or_create(status="réimpression")
s3, _ = LivreStatus.objects.using('mysql').get_or_create(status="en arrêt de commercialisation")

# Modifier le 2ème livre
l2 = Livre.objects.using('mysql').all()[1]
l2.status = s2
l2.save(using='mysql')

# Modifier le 3ème livre
l3 = Livre.objects.using('mysql').all()[2]
l3.status = s3
l3.save(using='mysql')

# Supprimer le dernier livre
Livre.objects.using('mysql').last().delete(using='mysql')

# Compter les livres restants
Livre.objects.using('mysql').count()
```

---

## 7. Les Vues (Views) et URLs

### 7.1 urls.py principal

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', bookOnline.views.index),
    path('backoffice', backoffice.views.index),
    path('backoffice/getProduct', backoffice.views.getProduct),
    path('backoffice/getDetails', backoffice.views.getDetails),
    path('bookOnline/getLivres', bookOnline.views.getLivres),
    path('bookOnline/getLivresFiltered', bookOnline.views.getLivresFiltered),
    path('bookOnline/getLivresStatus', bookOnline.views.getLivresStatus),
]
```

### 7.2 Toutes les routes disponibles

| URL | Description |
|---|---|
| `/` | Page d'accueil |
| `/admin/` | Panel d'administration Django |
| `/backoffice` | Index backoffice |
| `/backoffice/getProduct` | Liste des produits |
| `/backoffice/getDetails` | Détails des produits |
| `/bookOnline/getLivres` | Liste de tous les livres |
| `/bookOnline/getLivresFiltered` | Requêtes filtrées sur les livres |
| `/bookOnline/getLivresStatus` | Statuts des livres |

### 7.3 Exemple de vue — getDetails

```python
from django.http import HttpResponse
from .models import Product

def getDetails(request):
    productD = Product.objects.all()
    product_details = ""

    for p in productD:
        product_details += p.name + ": " + str(p.code) + " | "

    return HttpResponse("Details of the product : " + product_details)
```

> ⚠️ `str(p.code)` est obligatoire — Python ne peut pas concaténer un `int` avec une `str` directement.

### 7.4 Vue avec tableau HTML — getLivres

```python
from django.http import HttpResponse
from .models import Livre

def getLivres(request):
    livres = Livre.objects.using('mysql').all()

    html = """
        <h2>Liste des Livres</h2>
        <table border='1' cellpadding='8'>
            <tr><th>ID</th><th>Nom</th><th>Prix</th><th>Type</th><th>Status</th></tr>
    """
    for l in livres:
        html += f"""
            <tr>
                <td>{l.id}</td>
                <td>{l.nom}</td>
                <td>{l.prix} €</td>
                <td>{l.type.genre}</td>
                <td>{l.status.status}</td>
            </tr>
        """
    html += "</table>"

    return HttpResponse(html)
```

---

## 8. Les Données Créées

### 8.1 Produits (SQLite — base par défaut)

| ID | Nom | Code |
|---|---|---|
| 1 | ipod | 1234 |

### 8.2 LivreType (MySQL — base bookr)

| ID | Genre |
|---|---|
| 1 | roman |

### 8.3 LivreStatus (MySQL — base bookr)

| ID | Status |
|---|---|
| 1 | toujours publié |
| 2 | réimpression |
| 3 | en arrêt de commercialisation |

### 8.4 Livres (MySQL — base bookr)

| ID | Nom | Prix | Type | Status |
|---|---|---|---|---|
| 2 | Harry Potter | 19.99 € | roman | toujours publié |
| 3 | Les Misérables | 8.00 € | roman | réimpression |
| 4 | Madame Bovary | 7.00 € | roman | en arrêt de commercialisation |
| 5 | Honoré de Balzac | 11.00 € | roman | toujours publié |

---

## 9. Mise en ligne sur GitHub

### 9.1 Fichiers importants

| Fichier | Rôle |
|---|---|
| `.gitignore` | Exclut les fichiers inutiles |
| `README.md` | Présentation du projet |
| `DOCUMENTATION.md` | Documentation complète |
| `requirements.txt` | Liste des dépendances Python |

### 9.2 Générer requirements.txt

```bash
pip freeze > requirements.txt
```

### 9.3 Commandes Git

```bash
git init
git add .
git commit -m "first commit - Django Bookr app"
git branch -M main
git remote add origin https://github.com/tenyega/Bookr.git
git push -u origin main
```

### 9.4 Ajouter un tag de version

```bash
git tag -a v1.0 -m "Version 1.0 - Initial release"
git push origin v1.0
```

---

## 10. Concepts Clés à Retenir

| Concept | Explication simple |
|---|---|
| **Model** | Classe Python = Table en base de données |
| **Migration** | Traduit les modèles en vraies tables SQL |
| **QuerySet** | Liste d'objets retournée par une requête Django |
| **Foreign Key** | Lien entre deux tables (ex: Livre → LivreType) |
| **View** | Fonction Python qui gère une requête HTTP |
| **URL Pattern** | Associe une adresse web à une vue |
| **`using('mysql')`** | Spécifie quelle base de données utiliser |
| **`get_or_create()`** | Crée un objet seulement s'il n'existe pas déjà |
| **`str()`** | Convertit un entier en chaîne de caractères |
| **`__startswith`** | Filtre les objets commençant par une valeur |
| **`__contains`** | Filtre les objets contenant une valeur |
| **`__gte`** | Filtre les objets dont la valeur est >= à X |
| **`order_by('-prix')`** | Trie par prix décroissant (`-` = décroissant) |

---

*Projet Bookr — Master 2 Tableau de Bord — Mars 2026*
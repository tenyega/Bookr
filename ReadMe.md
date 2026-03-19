# 📚 Bookr — Django Web Application

A Django-based book management web application built as part of a Master 2 project.

## 🛠️ Tech Stack

- **Backend:** Python 3.13, Django
- **Database:** MySQL (via WAMP) + SQLite
- **Tools:** phpMyAdmin, Django Shell, IPython

## 📦 Models

- `Livre` — Book with name and price
- `LivreType` — Book genre (roman, polar, biographie, etc.)
- `LivreStatus` — Publication status (toujours publié, réimpression, etc.)
- `Product` — Product with name and code
- `ProductItem` — Product item with code and color

## ⚙️ Installation

### 1. Clone the repository
git clone https://github.com/yourusername/bookr.git
cd bookr

### 2. Create a virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

### 3. Install dependencies
pip install -r requirements.txt

### 4. Configure the database
Edit `bookr/settings.py` and update the `DATABASES` section with your MySQL credentials.

### 5. Run migrations
python manage.py migrate

### 6. Start the server
python manage.py runserver

## 🌐 Available Routes

| URL | Description |
|-----|-------------|
| `/` | Home page |
| `/admin/` | Django admin panel |
| `/backoffice` | Backoffice index |
| `/backoffice/getProduct` | List of products |
| `/backoffice/getDetails` | Product details |
| `/bookOnline/getLivres` | List of all books |
| `/bookOnline/getLivresFiltered` | Filtered book queries |
| `/bookOnline/getLivresStatus` | Book statuses |

## 👤 Author

Master 2 — Tableau de Bord Project  
March 2026
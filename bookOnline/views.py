
from django.http import HttpResponse
from .models import Livre
from .models import LivreStatus
# Create your views here.
# Création de la fonction index est obligatoire !
def index(request):
    return HttpResponse("<h1>Bonjour à tous !</h1>")


# This function is to get all the books at ones 
def getLivres(request):
    livres = Livre.objects.using('mysql').all()

    html = """
        <h2>Liste des Livres</h2>
        <table border='1' cellpadding='8' cellspacing='0'>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nom</th>
                    <th>Prix</th>
                    <th>Type</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
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

    html += """
            </tbody>
        </table>
    """

    return HttpResponse(html)

# This function gets the books based on the filters  
def getLivresFiltered(request):

    all_livres = Livre.objects.using('mysql').all()
    starts_with_L = Livre.objects.using('mysql').filter(nom__startswith="L")
    contains_miserables = Livre.objects.using('mysql').filter(nom__contains="Misérables")
    price_gte_10 = Livre.objects.using('mysql').filter(prix__gte=10)
    price_gte_10_published = Livre.objects.using('mysql').filter(prix__gte=10, status__status="toujours publié")
    most_expensive = Livre.objects.using('mysql').order_by('-prix').first()

    def make_table(title, queryset):
        html = f"<h2>{title}</h2>"
        html += "<table border='1' cellpadding='8' cellspacing='0'>"
        html += "<tr><th>ID</th><th>Nom</th><th>Prix</th><th>Type</th><th>Status</th></tr>"
        for l in queryset:
            html += f"<tr><td>{l.id}</td><td>{l.nom}</td><td>{l.prix} €</td><td>{l.type.genre}</td><td>{l.status.status}</td></tr>"
        html += "</table><br>"
        return html

    html = ""
    html += make_table("Tous les livres", all_livres)
    html += make_table("Commencent par L", starts_with_L)
    html += make_table("Contiennent Misérables", contains_miserables)
    html += make_table("Prix >= 10", price_gte_10)
    html += make_table("Prix >= 10 et toujours publié", price_gte_10_published)
    html += f"<h2>Livre le plus cher</h2><p>{most_expensive.nom} — {most_expensive.prix} €</p>"

    return HttpResponse(html)


def getLivresStatus(request):

    statuses = LivreStatus.objects.using('mysql').all()
    livres = Livre.objects.using('mysql').all()
    total = Livre.objects.using('mysql').count()

    html = "<h2>Liste des Status</h2>"
    html += "<table border='1' cellpadding='8'>"
    html += "<tr><th>ID</th><th>Status</th></tr>"
    for s in statuses:
        html += f"<tr><td>{s.id}</td><td>{s.status}</td></tr>"
    html += "</table><br>"

    html += "<h2>Livres avec leurs Status</h2>"
    html += "<table border='1' cellpadding='8'>"
    html += "<tr><th>ID</th><th>Nom</th><th>Prix</th><th>Status</th></tr>"
    for l in livres:
        html += f"<tr><td>{l.id}</td><td>{l.nom}</td><td>{l.prix} €</td><td>{l.status.status}</td></tr>"
    html += "</table><br>"

    html += f"<h2>Nombre total de livres : {total}</h2>"

    return HttpResponse(html)
from django.http import HttpResponse
from .models import Livre
from .models import LivreStatus

# ── shared layout helpers ─────────────────────────────────────────────────────

TAILWIND_CDN = '<script src="https://cdn.tailwindcss.com"></script>'

GOOGLE_FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&'
    'family=DM+Sans:wght@400;500&display=swap" rel="stylesheet">'
)

BASE_STYLE = """
<style>
  body { font-family: 'DM Sans', sans-serif; }
  h1, h2, h3 { font-family: 'Playfair Display', serif; }
  .fade-in { animation: fadeIn .5s ease both; }
  @keyframes fadeIn { from { opacity:0; transform:translateY(12px); } to { opacity:1; transform:none; } }
  tbody tr { transition: background .15s; }
  .nav-link {
    display: flex; align-items: center; gap: 6px;
    padding: 6px 14px; border-radius: 8px;
    font-size: 0.85rem; font-weight: 500;
    color: #d6d3cd; text-decoration: none;
    transition: background .15s, color .15s;
    white-space: nowrap;
  }
  .nav-link:hover { background: rgba(251,191,36,.15); color: #fbbf24; }
  .nav-link.active { background: rgba(251,191,36,.2); color: #fbbf24; }
  .nav-divider { width:1px; height:20px; background:#44403c; flex-shrink:0; }
</style>
"""

# ── nav definition ────────────────────────────────────────────────────────────
#  (url, label, emoji)
NAV_LINKS = [
    ("/",                               "Accueil",          "🏠"),
    ("/bookOnline",                     "Book Online",      "📖"),
    ("/bookOnline/getLivres",           "Livres",           "📚"),
    ("/bookOnline/getLivresFiltered",   "Filtres",          "🔍"),
    ("/bookOnline/getLivresStatus",     "Statuts",          "🏷️"),
    ("/backoffice",                     "Backoffice",       "⚙️"),
    ("/backoffice/getProduct",          "Produits",         "📦"),
    ("/backoffice/getDetails",          "Détails",          "🗂️"),
]

def _navbar(active_url: str = "") -> str:
    links_html = ""
    for i, (url, label, icon) in enumerate(NAV_LINKS):
        is_active = "active" if url == active_url else ""
        links_html += f'<a href="{url}" class="nav-link {is_active}">{icon} {label}</a>'
        # divider between bookOnline group and backoffice group
        if i == 4:
            links_html += '<span class="nav-divider"></span>'

    return f"""
<header class="bg-stone-900 text-stone-100 shadow-lg sticky top-0 z-50">
  <div class="max-w-7xl mx-auto px-6 py-3 flex items-center gap-2 overflow-x-auto">
    <!-- Brand -->
    <a href="/" class="flex items-center gap-2 mr-4 flex-shrink-0">
      <span class="text-amber-400 text-xl">📚</span>
      <span class="text-lg font-bold tracking-wide text-white" style="font-family:'Playfair Display',serif;">
        Bibliothèque
      </span>
    </a>
    <span class="nav-divider mr-2"></span>
    <!-- Nav links -->
    {links_html}
  </div>
</header>"""


def _page(title: str, body: str, active_url: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} · Bibliothèque</title>
  {TAILWIND_CDN}
  {GOOGLE_FONTS}
  {BASE_STYLE}
</head>
<body class="min-h-screen bg-stone-50 text-stone-800">

  {_navbar(active_url)}

  <main class="max-w-6xl mx-auto px-6 py-10 fade-in">
    {body}
  </main>

  <footer class="text-center text-stone-400 text-xs py-8">
    © Bibliothèque Django · Tailwind CSS
  </footer>

</body>
</html>"""


# ── reusable UI components ────────────────────────────────────────────────────

def _table(headers: list[str], rows: list[list], accent: str = "amber") -> str:
    th_cls = f"px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-{accent}-700 bg-{accent}-50"
    td_cls = "px-4 py-3 text-sm text-stone-700"

    head_cells = "".join(f'<th class="{th_cls}">{h}</th>' for h in headers)
    body_rows  = ""
    for i, row in enumerate(rows):
        bg = "bg-white" if i % 2 == 0 else "bg-stone-50"
        cells = "".join(f'<td class="{td_cls}">{cell}</td>' for cell in row)
        body_rows += f'<tr class="{bg} hover:bg-{accent}-50/60">{cells}</tr>'

    return f"""
<div class="overflow-x-auto rounded-xl border border-stone-200 shadow-sm">
  <table class="min-w-full divide-y divide-stone-200">
    <thead><tr>{head_cells}</tr></thead>
    <tbody class="divide-y divide-stone-100">{body_rows}</tbody>
  </table>
</div>"""


def _section_title(text: str) -> str:
    return f"""
<h2 class="text-2xl font-bold text-stone-800 mb-4 mt-8 border-l-4 border-amber-400 pl-3">
  {text}
</h2>"""


def _stat_card(label: str, value: str, icon: str = "📖") -> str:
    return f"""
<div class="bg-white rounded-xl border border-stone-200 shadow-sm px-6 py-5 flex items-center gap-4">
  <span class="text-3xl">{icon}</span>
  <div>
    <p class="text-xs uppercase tracking-wide text-stone-400 font-medium">{label}</p>
    <p class="text-xl font-bold text-stone-800">{value}</p>
  </div>
</div>"""


def _quick_links() -> str:
    """Grid of shortcut cards shown on the index page."""
    cards = [
        ("/bookOnline",                   "Book Online",            "📖", "Accéder au catalogue en ligne"),
        ("/bookOnline/getLivres",         "Tous les livres",        "📚", "Voir l'ensemble du catalogue"),
        ("/bookOnline/getLivresFiltered", "Livres filtrés",         "🔍", "Recherches et filtres avancés"),
        ("/bookOnline/getLivresStatus",   "Statuts des livres",     "🏷️", "Livres classés par statut"),
        ("/backoffice",                   "Backoffice",             "⚙️", "Administration générale"),
        ("/backoffice/getProduct",        "Produits",               "📦", "Gérer les produits"),
        ("/backoffice/getDetails",        "Détails produits",       "🗂️", "Voir les détails"),
    ]
    items = ""
    for url, title, icon, desc in cards:
        items += f"""
<a href="{url}"
   class="group bg-white rounded-xl border border-stone-200 shadow-sm hover:shadow-md
          hover:border-amber-300 transition-all p-5 flex flex-col gap-2">
  <span class="text-3xl">{icon}</span>
  <p class="font-semibold text-stone-800 group-hover:text-amber-600 transition-colors">{title}</p>
  <p class="text-xs text-stone-400">{desc}</p>
</a>"""
    return f'<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mt-6">{items}</div>'


# ── views ──────────────────────────────────────────────────────────────────────

def index(request):
    body = f"""
<div class="mb-8">
  <h1 class="text-4xl font-bold text-stone-800 mb-2">Bonjour à tous&nbsp;! 👋</h1>
  <p class="text-stone-500">Bienvenue dans l'application Bibliothèque. Choisissez une section ci-dessous.</p>
</div>
{_quick_links()}"""
    return HttpResponse(_page("Accueil", body, active_url="/"))


def getBookOnline(request):
    body = """
<div class="flex flex-col items-center justify-center py-20 gap-4 text-center">
  <span class="text-6xl">📖</span>
  <h1 class="text-4xl font-bold text-stone-800">Book Online</h1>
  <p class="text-stone-500 max-w-md">
    Explorez le catalogue, consultez les livres disponibles et filtrez par statut ou prix.
  </p>
  <div class="flex flex-wrap gap-3 mt-4 justify-center">
    <a href="/bookOnline/getLivres"
       class="bg-amber-400 hover:bg-amber-500 text-stone-900 font-semibold px-5 py-2.5 rounded-lg transition-colors text-sm">
      📚 Tous les livres
    </a>
    <a href="/bookOnline/getLivresFiltered"
       class="border border-stone-300 hover:border-amber-400 text-stone-700 font-medium px-5 py-2.5 rounded-lg transition-colors text-sm">
      🔍 Livres filtrés
    </a>
    <a href="/bookOnline/getLivresStatus"
       class="border border-stone-300 hover:border-amber-400 text-stone-700 font-medium px-5 py-2.5 rounded-lg transition-colors text-sm">
      🏷️ Statuts
    </a>
  </div>
</div>"""
    return HttpResponse(_page("Book Online", body, active_url="/bookOnline"))


def getLivres(request):
    livres = Livre.objects.using('mysql').all()
    rows = [[l.id, l.nom, f"{l.prix} €", l.type.genre, l.status.status] for l in livres]
    body = _section_title("Liste des Livres") + _table(["ID", "Nom", "Prix", "Type", "Status"], rows)
    return HttpResponse(_page("Liste des livres", body, active_url="/bookOnline/getLivres"))


def getLivresFiltered(request):
    all_livres             = Livre.objects.using('mysql').all()
    starts_with_L          = Livre.objects.using('mysql').filter(nom__startswith="L")
    contains_miserables    = Livre.objects.using('mysql').filter(nom__contains="Misérables")
    price_gte_10           = Livre.objects.using('mysql').filter(prix__gte=10)
    price_gte_10_published = Livre.objects.using('mysql').filter(
                                 prix__gte=10, status__status="toujours publié")
    most_expensive         = Livre.objects.using('mysql').order_by('-prix').first()

    def qs_rows(qs):
        return [[l.id, l.nom, f"{l.prix} €", l.type.genre, l.status.status] for l in qs]

    headers = ["ID", "Nom", "Prix", "Type", "Status"]
    sections = [
        ("Tous les livres",                all_livres,             "amber"),
        ("Commencent par « L »",           starts_with_L,          "sky"),
        ("Contiennent « Misérables »",     contains_miserables,    "violet"),
        ("Prix ≥ 10 €",                    price_gte_10,           "emerald"),
        ("Prix ≥ 10 € et toujours publié", price_gte_10_published, "rose"),
    ]

    body = ""
    for title, qs, accent in sections:
        body += _section_title(title) + _table(headers, qs_rows(qs), accent=accent)

    body += _section_title("Livre le plus cher")
    body += _stat_card(label=most_expensive.nom, value=f"{most_expensive.prix} €", icon="🏆")

    return HttpResponse(_page("Livres filtrés", body, active_url="/bookOnline/getLivresFiltered"))


def getLivresStatus(request):
    statuses = LivreStatus.objects.using('mysql').all()
    livres   = Livre.objects.using('mysql').all()
    total    = Livre.objects.using('mysql').count()

    body = f"""
<div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">
  {_stat_card("Total des livres", str(total), "📚")}
  {_stat_card("Statuts disponibles", str(statuses.count()), "🏷️")}
</div>"""

    status_rows = [[s.id, s.status] for s in statuses]
    body += _section_title("Liste des Statuts")
    body += _table(["ID", "Statut"], status_rows, accent="violet")

    livre_rows = [[l.id, l.nom, f"{l.prix} €", l.status.status] for l in livres]
    body += _section_title("Livres avec leurs Statuts")
    body += _table(["ID", "Nom", "Prix", "Statut"], livre_rows, accent="amber")

    return HttpResponse(_page("Statuts des livres", body, active_url="/bookOnline/getLivresStatus"))
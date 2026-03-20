from django.http import HttpResponse
from .models import Product, ProductItem

# ── shared layout helpers (same theme as bookOnline) ──────────────────────────

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

NAV_LINKS = [
    ("/",                               "Accueil",      "🏠"),
    ("/bookOnline",                     "Book Online",  "📖"),
    ("/bookOnline/getLivres",           "Livres",       "📚"),
    ("/bookOnline/getLivresFiltered",   "Filtres",      "🔍"),
    ("/bookOnline/getLivresStatus",     "Statuts",      "🏷️"),
    ("/backoffice",                     "Backoffice",   "⚙️"),
    ("/backoffice/getProduct",          "Produits",     "📦"),
    ("/backoffice/getDetails",          "Détails",      "🗂️"),
]

def _navbar(active_url: str = "") -> str:
    links_html = ""
    for i, (url, label, icon) in enumerate(NAV_LINKS):
        is_active = "active" if url == active_url else ""
        links_html += f'<a href="{url}" class="nav-link {is_active}">{icon} {label}</a>'
        if i == 4:
            links_html += '<span class="nav-divider"></span>'

    return f"""
<header class="bg-stone-900 text-stone-100 shadow-lg sticky top-0 z-50">
  <div class="max-w-7xl mx-auto px-6 py-3 flex items-center gap-2 overflow-x-auto">
    <a href="/" class="flex items-center gap-2 mr-4 flex-shrink-0">
      <span class="text-amber-400 text-xl">📚</span>
      <span class="text-lg font-bold tracking-wide text-white" style="font-family:'Playfair Display',serif;">
        Bibliothèque
      </span>
    </a>
    <span class="nav-divider mr-2"></span>
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


def _section_title(text: str) -> str:
    return f"""
<h2 class="text-2xl font-bold text-stone-800 mb-4 mt-8 border-l-4 border-amber-400 pl-3">
  {text}
</h2>"""


def _stat_card(label: str, value: str, icon: str = "📦") -> str:
    return f"""
<div class="bg-white rounded-xl border border-stone-200 shadow-sm px-6 py-5 flex items-center gap-4">
  <span class="text-3xl">{icon}</span>
  <div>
    <p class="text-xs uppercase tracking-wide text-stone-400 font-medium">{label}</p>
    <p class="text-xl font-bold text-stone-800">{value}</p>
  </div>
</div>"""


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


# ── views ──────────────────────────────────────────────────────────────────────

def index(request):
    cards = [
        ("/backoffice/getProduct", "Produits",        "📦", "Voir la liste de tous les produits"),
        ("/backoffice/getDetails", "Détails produits","🗂️", "Codes et informations détaillées"),
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

    body = f"""
<div class="mb-8">
  <div class="inline-flex items-center gap-2 bg-amber-50 border border-amber-200 text-amber-700
              text-xs font-semibold px-3 py-1 rounded-full mb-4 uppercase tracking-wide">
    ⚙️ Administration
  </div>
  <h1 class="text-4xl font-bold text-stone-800 mb-2">Backoffice</h1>
  <p class="text-stone-500">Gérez les produits et consultez les détails de la base de données.</p>
</div>
<div class="grid grid-cols-1 sm:grid-cols-2 gap-4">{items}</div>"""

    return HttpResponse(_page("Backoffice", body, active_url="/backoffice"))


def getProduct(request):
    products = Product.objects.all()
    total    = products.count()

    rows = [[i + 1, p.name] for i, p in enumerate(products)]

    body = f"""
<div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-2">
  {_stat_card("Total des produits", str(total), "📦")}
</div>
{_section_title("Liste des Produits")}
{_table(["#", "Nom du produit"], rows, accent="amber")}"""

    return HttpResponse(_page("Produits", body, active_url="/backoffice/getProduct"))


def getDetails(request):
    products = Product.objects.all()
    total    = products.count()

    rows = [[i + 1, p.name, p.code] for i, p in enumerate(products)]

    body = f"""
<div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-2">
  {_stat_card("Total des produits", str(total), "🗂️")}
</div>
{_section_title("Détails des Produits")}
{_table(["#", "Nom du produit", "Code"], rows, accent="stone")}"""

    return HttpResponse(_page("Détails produits", body, active_url="/backoffice/getDetails"))
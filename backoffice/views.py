# Create your views here.
from django.http import HttpResponse
from .models import Product, ProductItem

def index(request):
    return HttpResponse("<h1>Bonjour à tous sur le backoffice app !</h1>")

def getProduct(request):
    product = Product.objects.all()
    product_str = ""

    for p in product:
        product_str += p.name + ", "

    return HttpResponse("Liste des produits we have found in db  : " + product_str)

def getDetails(request):
    productD = Product.objects.all()
    product_details = ""

    for p in productD:
        product_details += p.name + ": " + str(p.code) + " | "

    return HttpResponse("Details of the product : " + product_details)
from django.contrib import admin


from .models import Livre, LivreStatus, LivreType
admin.site.register(LivreStatus)
admin.site.register(Livre)
admin.site.register(LivreType)  
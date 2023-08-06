from django.contrib import admin

from .models import Faq, Collective, Testimony, Event, Client

admin.site.register(Faq)
admin.site.register(Collective)
admin.site.register(Testimony)
admin.site.register(Event)
admin.site.register(Client)
from django.contrib import admin
from .models import *

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass



# from django.contrib import admin
# from .models import *

# from .models import Electronics, OperatingSystem





# class ElectronicsAdmin(admin.ModelAdmin):
#     # le colonnine 
#     list_display = ('id', 'title', 'content', 'time_create', 'time_update')
    
#     # quali dei dati nelle colonnine son sono linkati
#     list_display_links = ('id', 'title')
    
#     # parametri di ricerca che si deve fare 
#     search_fields = ('title', 'content')
#     list_filter = ('time_create', 'time_update')
    
# class OperatingSystemAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title')
    
    
    
    
# admin.site.register(OperatingSystem)   
# admin.site.register(Electronics, ElectronicsAdmin)



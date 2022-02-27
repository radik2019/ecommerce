from django.urls import path
from .views import *


urlpatterns = [
    path("products/", ProductView.as_view(), name="products"),
    path("products/<int:pk>/", ProductView.as_view(), name="products"),
    
    path("brands/", BrandView.as_view(), name="brands"),
    path("brands/<int:pk>/", BrandView.as_view(), name="brands"),
    
    path('categories/', CategoryView.as_view(), name="categories"),
    path('categories/<int:pk>/', CategoryView.as_view(), name="categories"),
]

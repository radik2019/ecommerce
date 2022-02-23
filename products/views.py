from django.views.generic import View
from django.forms.models import model_to_dict
from django.http.response import JsonResponse
from .models import *
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name="dispatch")
class ProductView(View):
    def get(self, request, pk=None, *args, **kwargs):
        if not pk:
            collection = Product.objects.all()
            to_serialize = [*map(lambda m: model_to_dict(m), collection)]
            return JsonResponse(to_serialize, status=200, safe=False)
        resource = Product.objects.filter(pk=pk)
        if not resource.exists():
            return JsonResponse({"detail": "product not found"}, status=404)
        return JsonResponse(model_to_dict(resource.first()), status=200, safe=False)
    
    def post(self, request):
        print(request.body)
        task = None
        try:
            req_payload = json.loads(request.body)
            print(req_payload)
            
            task_name = req_payload.get("name", None)
            task_price = req_payload.get("price", "")
            task_availability = int(req_payload.get("availability"))
            task_category = req_payload.get("category")
            task_brand = req_payload.get("brand")

            task = Product.objects.create(
                name=task_name,
                price=task_price,
                availability=task_availability,
                category=task_category,
                brand=task_brand
            )
        except Exception as e:
            print(e) # Stampo nel log del server l'eccezione, qualunque essa sia
            return JsonResponse(
                {"error": "Errore nella creazione del modello"},
                status=500
            )
            
        res_payload = {
            "id": task.pk,
            "name": task.name,
            "price": task.price,
            "availability": task.availability,
            "category_id": task.category.pk,
            "brand_id": task.brand.pk,

        }

        return JsonResponse(res_payload, status=201)

class BrandView(View):
    def get(self, request, pk=None, *args, **kwargs):
        if not pk:
            collection = Brand.objects.all()
            to_serialize = [*map(lambda m: model_to_dict(m), collection)]
            return JsonResponse(to_serialize, status=200, safe=False)
        resource = Brand.objects.filter(pk=pk)
        if not resource.exists():
            return JsonResponse({"detail": "brand not found"}, status=404)
        return JsonResponse(model_to_dict(resource.first()), status=200, safe=False)
    
class CategoryView(View):
    def get(self, request, pk=None, *args, **kwargs):
        if not pk:
            collection = Category.objects.all()
            to_serialize = [*map(lambda m: model_to_dict(m), collection)]
            return JsonResponse(to_serialize, status=200, safe=False)
        resource = Category.objects.filter(pk=pk)
        if not resource.exists():
            return JsonResponse({"detail": "category not found"}, status=404)
        return JsonResponse(model_to_dict(resource.first()), status=200, safe=False)


    

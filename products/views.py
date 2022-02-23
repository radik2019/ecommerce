from django.views.generic import View
from django.forms.models import model_to_dict
from django.http.response import JsonResponse
from .models import Product, Brand, Category
import json
from django.views.decorators.csrf import csrf_exempt

class RetrieveRESTViewMixin:
    def get_detail(self, request, pk=None, *args, **kwargs):
        resource = self.model.objects.filter(pk=pk) # Retrieve
        if not resource.exists():
            return JsonResponse({"detail": "Resource not found"}, status=404)
        return JsonResponse(model_to_dict(resource.first()), status=200, safe=False)


class ListRESTViewMixin:
    def get_list(self, request, *args, **kwargs):
        collection = self.model.objects.all()
        to_serialize = [*map(lambda m: model_to_dict(m), collection)]
        return JsonResponse(to_serialize, status=200, safe=False)


class RESTView(View):
    model = None

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            if request.method.lower() == "get":
                if "pk" in kwargs.keys():
                    handler = getattr(self, "get_detail", self.http_method_not_allowed)
                else:
                    handler = getattr(self, "get_list", self.http_method_not_allowed)
            else:
                handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({"detail": "Method not allowed!"}, status=405)


class ProductView(RESTView, ListRESTViewMixin, RetrieveRESTViewMixin):
    model = Product 
    
    def post(self, request):
        print(request.body)
        task = None
        try:
            req_payload = json.loads(request.body)
            print(req_payload)
            
            task_name = req_payload.get("name")
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
            
        # res_payload = {
        #     "id": task.pk,
        #     "name": task.name,
        #     "price": task.price,
        #     "availability": task.availability,
        #     "category_id": task.category.pk,
        #     "brand_id": task.brand.pk,

        # }

        return JsonResponse(model_to_dict(task), status=201)

class BrandView(RESTView, ListRESTViewMixin):
    model = Brand




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
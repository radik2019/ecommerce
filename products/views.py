from django.views.generic import View
from django.forms.models import model_to_dict
from django.http.response import JsonResponse
from .models import Product, Brand, Category
import json
from django.views.decorators.csrf import csrf_exempt

def debug_(s):
    print("*" * 50, "\n", s, '\n', "*" * 50)

class RetrieveRESTViewMixin:
    def get_detail(self, request, pk=None, *args, **kwargs):
        resource = self.model.objects.filter(pk=pk) # Retrieve
        if not resource.exists():
            return JsonResponse({"detail": "Resource not found"}, status=404)
        return JsonResponse(model_to_dict(resource.first()), status=200, safe=False)

class DeleteRESTViewMixin:
    def del_detail(self, request, pk=None, *args, **kwargs):
        resource = self.model.objects.filter(pk=pk)  # Retrieve
        if not resource.exists():
            return JsonResponse({"detail": "Resource not found"}, status=404)
        resource_name = resource.first()
        resource_name.first().delete()
        return JsonResponse({"detail": f"[{resource_name}] has been deleted"}, status=200, safe=False)

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
            elif request.method.lower() == "delete":
                handler = getattr(self, "del_detail", self.http_method_not_allowed)
            else:
                handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({"detail": "Method not allowed!"}, status=405)




class ProductView(RESTView, ListRESTViewMixin, RetrieveRESTViewMixin, DeleteRESTViewMixin):
    model = Product 
    
    def post(self, request):
        """
        {
        "name": "Galaxy S4",       # string
        "price": 200.01,           # float
        "availability": 10,        # int
        "category": "Elettronica", # str (existing category)
        "brand": "Samsung"         # str (existing brand)
        }
        """
        task = None
        try:
            req_payload = json.loads(request.body)
            task = Product.objects.create(
                name=req_payload.get("name"),
                price=req_payload.get("price", ""),
                availability=int(req_payload.get("availability")),
                category=Category.objects.get(cat_name=req_payload.get("category")),
                brand=Brand.objects.get(model_name=req_payload.get("brand"))
            )
        except Exception as e:
            print(e)
            return JsonResponse(
                {"error": "Errore nella creazione del modello"},
                status=500
            )
        return JsonResponse(model_to_dict(task), status=201)



class BrandView(RESTView, ListRESTViewMixin, RetrieveRESTViewMixin, DeleteRESTViewMixin):
    model = Brand


class CategoryView(RESTView, ListRESTViewMixin, RetrieveRESTViewMixin, DeleteRESTViewMixin):
    model = Category

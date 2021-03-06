from venv import create
from django.views.generic import View
from django.forms.models import model_to_dict
from django.http.response import JsonResponse
from .models import Product, Brand, Category
import json
from hashlib import sha256
from django.views.decorators.csrf import csrf_exempt


def debug_(s):
    import os
    width_wind = os.get_terminal_size().columns - 5
    print("*" * width_wind, "\n\n", s, '\n\n' + "*" * width_wind)


class RetrieveRESTViewMixin:
    def get_detail(self, request, pk=None, *args, **kwargs):
        resource = self.model.objects.filter(pk=pk)  # Retrieve
        if not resource.exists():
            return JsonResponse({"detail": "Resource not found"}, status=404)
        return JsonResponse(model_to_dict(resource.first()), status=200, safe=False)


class DeleteRESTViewMixin:
    def del_detail(self, request, pk=None, *args, **kwargs):
        resource = self.model.objects.filter(pk=pk)  # Retrieve
        if not resource.exists():
            return JsonResponse({"detail": "Resource not found"}, status=404)
        resource_name = resource.first()
        try:
            resource_name.delete()
        except ProtectedError:
            return JsonResponse({"error": "Cannot delete some instances of model" /
                                 "because they are referenced through protected foreign keys"},
                                status=500)
        return JsonResponse({"detail": f"[{resource_name}] has been deleted"}, status=200, safe=False)


class CreateRESTViewMixin:
    def create_detail(self, request, *args, **kwargs):
        req_payload = json.loads(request.body)
        try:
            self.model.objects.create(name=req_payload.get("name"))
        except Exception as e:
            print(e)
            return JsonResponse({"error": "Errore nella modifica del modello"}, status=500)
        return JsonResponse(model_to_dict(self.model.objects.get(name=req_payload["name"])), status=201)


class ListRESTViewMixin:
    def get_list(self, request, *args, **kwargs):
        collection = self.model.objects.all()
        to_serialize = [*map(lambda m: model_to_dict(m), collection)]
        return JsonResponse(to_serialize, status=200, safe=False)


class UpdateRESTViewMixin:
    def update_detail(self, request, *args, **kwargs):
        req_payload = json.loads(request.body)
        try:
            obj = self.model.objects.filter(pk=req_payload.get("id"))
            obj.update(name=req_payload.get("name"))
        except Exception as e:
            print(e)
            return JsonResponse({"error": "Errore nella modifica del modello"}, status=500)
        return JsonResponse(model_to_dict(self.model.objects.get(pk=req_payload["id"])), status=201)


class RESTView(View):
    model = None

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            if request.method.lower() == "get":
                if "pk" in kwargs.keys():
                    handler = getattr(self, "get_detail",
                                      self.http_method_not_allowed)
                else:
                    handler = getattr(self, "get_list",
                                      self.http_method_not_allowed)
            elif request.method.lower() == "delete":
                handler = getattr(self, "del_detail",
                                  self.http_method_not_allowed)
            elif request.method.lower() == "post":
                handler = getattr(self, "create_detail",
                                  self.http_method_not_allowed)
            elif request.method.lower() == "put":
                handler = getattr(self, "update_detail",
                                  self.http_method_not_allowed)
            else:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({"detail": "Method not allowed!"}, status=405)


class ProductView(RESTView,
                  ListRESTViewMixin,
                  RetrieveRESTViewMixin,
                  DeleteRESTViewMixin):
    model = Product

    def hash_product(self, req_payload):
        name: str = req_payload.get("name")
        category = Category.objects.get(pk=req_payload.get("category")).name
        brand = Brand.objects.get(pk=req_payload.get("brand")).name
        s = (name + category + brand).encode(encoding='utf-8')
        hashed = sha256(s).hexdigest()
        return hashed

    def post(self, request):
        """
        {
        "name": "product_name",  # string
        "price": 200.01,      # float
        "availability": 10,   # int
        "category": 3,        # int (id category)
        "brand": 4            # int (id brand)
        }
        """
        task = None
        try:
            req_payload = json.loads(request.body)
            task = Product.objects.create(
                hash_summ=self.hash_product(req_payload),
                name=req_payload.get("name"),
                price=req_payload.get("price"),
                availability=int(req_payload.get("availability")),
                category=Category.objects.get(pk=req_payload.get("category")),
                brand=Brand.objects.get(pk=req_payload.get("brand"))
            )
        except Exception as e:
            print(e)
            return JsonResponse(
                {"error": "Errore nella creazione del modello"},
                status=500
            )
        return JsonResponse(model_to_dict(task), status=201)

    def put(self, request, *args):
        """_summary_
        {
            "id": 8, # id da modificare
            "name": "updated_product_name",
            "price": 4.01,
            "availability": 10,
            "category": 2,
            "brand": 5
        }
        """
        req_payload = json.loads(request.body)
        try:
            product_obj = Product.objects.filter(pk=req_payload.get("id"))

            product_obj.update(hash_summ=self.hash_product(req_payload))
            product_obj.update(name=req_payload.get("name"))
            product_obj.update(price=req_payload.get("price"))
            product_obj.update(availability=req_payload.get("availability"))
            product_obj.update(category=Category.objects.get(
                pk=req_payload.get("category"))),
            product_obj.update(brand=Brand.objects.get(
                pk=req_payload.get("brand")))

        except Exception as e:
            print(e)
            return JsonResponse({"error": "Errore nella modifica del modello"}, status=500)
        return JsonResponse(model_to_dict(Product.objects.get(pk=req_payload["id"])), status=201)


class BrandView(RESTView,
                ListRESTViewMixin,
                RetrieveRESTViewMixin,
                DeleteRESTViewMixin,
                CreateRESTViewMixin,
                UpdateRESTViewMixin):
    model = Brand
    """
        --- PUT --
    {"name": "modified_brand_name"}
    
        --- POST ---
    {"name": "category_name"}
    """


class CategoryView(RESTView,
                   ListRESTViewMixin,
                   RetrieveRESTViewMixin,
                   DeleteRESTViewMixin,
                   CreateRESTViewMixin,
                   UpdateRESTViewMixin):
    model = Category
    """
        --- PUT --
    {"name": "modified_category_name"}
    
        --- POST ---
    {"name": "category_name"}
    """

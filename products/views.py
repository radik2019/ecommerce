from django.views.generic import View
from django.forms.models import model_to_dict
from django.http.response import JsonResponse
from .models import Product


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





# Create your views here.

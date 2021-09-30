import json

from debugger import query_debugger
from django.views import View
from django.http  import JsonResponse

from products.models import Product, Summary, Image

class ProductView(View):
    def get(self, request):
        try:
            products = Product.objects.all().prefetch_related('summary_set')
        
            result   = [{
                'id'       : product.id,
                'name'     : product.name,
                'sub_name' : product.sub_name,
                'price'    : product.price,
                'image'    : product.image_set.first().image_url,
                'summary'  : [summary.name for summary in product.summary_set.all()]
            }for product in products]

            return JsonResponse({"Result" : result}, status=200)
        except AttributeError:
            return JsonResponse({"message" : "IMAGE_NOT_FOUND"}, status=400)

class ProductDetailView(View):
    def get(self, request):
        try:
            product_id = request.GET.get('id')
            product    = Product.objects.get(id=product_id)
            
            result = {
                'id'              : product.id,
                'name'            : product.name,
                'sub_name'        : product.sub_name,
                'price'           : product.price,
                'description'     : product.description,
                'sub_description' : product.sub_description,
                'image'           : product.image_set.first().image_url,
                'background_image': product.image_set.last().image_url
            }
            return JsonResponse({"Result" : result}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({"message" : "PRODUCT_NOT_FOUND"}, status=400)
        except AttributeError:
            return JsonResponse({"message" : "IMAGE_NOT_FOUND"}, status=400)


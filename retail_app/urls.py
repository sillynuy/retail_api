from django.urls import include, path
from rest_framework import routers

from retail_app.views import *

router = routers.DefaultRouter()
# router.register(r'v1/stores', StoreViewSet)
# router.register(r'v1/remains', RemainViewSet)
# router.register(r'v1/products', ProductViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path('v1/stores/', stores_list),
    path('v1/stores/<int:store_id>/', stores_detailed),
    path('v1/stores/<int:store_id>/add', add_to_store),
    path('v1/stores/<int:store_id>/buy', buy_from_store)
]

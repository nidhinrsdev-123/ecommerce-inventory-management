from django.contrib import admin
from django.urls import include,path
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView
from shop.views import ProductViewSet,OrderViewSet
router=DefaultRouter(); router.register("products",ProductViewSet,basename="product"); router.register("orders",OrderViewSet,basename="order")
urlpatterns=[path("admin/",admin.site.urls),path("api/",include(router.urls)),path("api/schema/",SpectacularAPIView.as_view(),name="schema"),path("api/docs/",SpectacularSwaggerView.as_view(url_name="schema"),name="swagger-ui")]

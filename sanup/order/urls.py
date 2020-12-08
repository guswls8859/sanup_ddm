from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt
from . import views
from rest_framework import routers

app_name = 'order'

router = routers.DefaultRouter()
router.register(r'order_design_data', views.Order_design_data_api, basename='order_design_data_apis')
router1 = routers.DefaultRouter()
router1.register(r'order_data', views.Order_api, basename='order_data_apis')

urlpatterns = [
    url(r'^rawroll/(?P<id>\d+)', views.rawroll),
    url(r'^warpWorkSheet/(?P<id>\d+)', views.warpTable),
    url(r'^modify$', views.modifyOrder),
    url(r'^delete$', views.delete),
    url(r'^$', views.order),
    url(r'^list$', views.getOrderListByJson),
    url(r'^detail/(?P<orderId>\d+)', views.getOrderByJson),
    url(r'^showQr/(?P<id>\d+)', views.showQr),
    url(r'^subOrderJson/(?P<id>\d+)', views.getSubOrderByJson),
    url(r'^ordercheack$', views.ordercheack),
    url(r'^design_api/', include(router.urls, 'Order_design'), name='design_api'),
    url(r'^order_api/', include(router1.urls, 'Order'), name='order_api'),
]
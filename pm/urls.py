from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from azbankgateways.urls import az_bank_gateways_urls
from account.views import callback_gateway_view, go_to_gateway_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls', namespace='account')),
    path('ticket/', include('ticket.urls', namespace='ticket')),
    path('', include('product.urls', namespace='product')),
    path('order/', include('order.urls', namespace='order')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('api/', include('api.urls', namespace='api')),
    # third_apps
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # payment
    path('bankgateways/', az_bank_gateways_urls()),
    path('payment/<int:order_id>/', go_to_gateway_view, name='payment'),
    path('callback-gateway/<int:order_id>/', callback_gateway_view, name='callback-gateway'),
    # end payment

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                        document_root=settings.
                                                                                        MEDIA_ROOT)

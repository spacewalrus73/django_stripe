from django.urls import path
from django.contrib import admin
from product.views import (
    CreateCheckoutSessionView,
    ProductPageView,
    SuccessPageView,
    CancelPageView,
    StripeIntentView,
    OrderPageView,
    CreateOrderCheckoutSessionView,
    StripeOrderIntentView,
    home_page_view,
)

urlpatterns = [
    path('', home_page_view, name='root'),
    path('admin/', admin.site.urls),
    path('success/', SuccessPageView.as_view(), name="success_page"),
    path('cancel/', CancelPageView.as_view(), name="cancel_page"),
    # Item urls
    path('item/<int:id>/', ProductPageView.as_view(), name='product_view'),
    path('buy/<int:id>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('create-payment-intent/<int:id>/', StripeIntentView.as_view(), name='create-payment-intent'),
    # Order urls
    path('order/<int:id>/', OrderPageView.as_view(), name='order_view'),
    path('buyorder/<int:id>/', CreateOrderCheckoutSessionView.as_view(), name='order-checkout-session'),
    path('create-order-payment-intent/<int:id>/', StripeOrderIntentView.as_view(), name='create-order-payment-intent'),
]

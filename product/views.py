import stripe
from django.views import View
from product.models import Order, Item
from django.conf import settings
from django.shortcuts import redirect, render
from django.http import Http404, JsonResponse
from django.views.generic import TemplateView


stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductPageView(TemplateView):
    template_name = 'landing_item.html'

    def get_context_data(self, **kwargs):
        try:
            item = Item.objects.get(id=kwargs.get('id'))
        except Exception:
            raise Http404
        context = super(ProductPageView, self).get_context_data(**kwargs)
        context['item'] = item
        context['STRIPE_PUBLIC_KEY'] = settings.STRIPE_PUBLIC_KEY
        context['domain'] = settings.DOMAIN
        return context


class CreateCheckoutSessionView(View):

    def get(self, request, *args, **kwargs):
        item = Item.objects.get(id=kwargs.get('id'))
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': item.currency,
                        'product_data': {
                            'name': item.name,
                        },
                        'unit_amount': item.price,
                    },
                    'quantity': 1,
                }
            ],
            mode='payment',
            automatic_tax={'enabled': True},
            success_url=settings.DOMAIN + '/success/',
            cancel_url=settings.DOMAIN + '/cancel/',
        )
        # return JsonResponse({'id': checkout_session.id}) deprecated
        return redirect(checkout_session.url, code=303)


class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            item = Item.objects.get(id=self.kwargs.get('id'))
            intent = stripe.PaymentIntent.create(
                amount=item.price,
                currency=item.currency,
                payment_method_types=['card'],
                # automatic_payment_methods={
                #     'enabled': True,
                # }
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})


class OrderPageView(TemplateView):
    template_name = 'landing_order.html'

    def get_context_data(self, **kwargs):
        try:
            order = Order.objects.get(id=kwargs.get('id'))
        except Exception:
            raise Http404
        context = super(OrderPageView, self).get_context_data(**kwargs)
        context['order'] = order
        context['STRIPE_PUBLIC_KEY'] = settings.STRIPE_PUBLIC_KEY
        context['domain'] = settings.DOMAIN
        return context


class CreateOrderCheckoutSessionView(View):
    def get(self, request, *args, **kwargs):
        order = Order.objects.get(id=kwargs.get('id'))
        tax = stripe.TaxRate.create(
            display_name=order.tax.tax_name,
            inclusive=order.tax.inclusive,
            percentage=order.tax.percentage,
        )
        try:
            stripe.Coupon.create(
                id=order.discount.id,
                percent_off=order.discount.percentage,
                duration=order.discount.duration,
            )
        except Exception:
            pass

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': item.currency,
                        'product_data': {
                            'name': item.name,
                        },
                        'unit_amount': item.price,
                        'tax_behavior': 'inclusive' if tax.inclusive
                                        else 'unspecified',
                    },
                    'quantity': 1,
                    'tax_rates': [tax.id],
                } for item in order.items.all()
            ],
            discounts=[{"coupon": order.discount.id}],
            mode='payment',
            success_url=settings.DOMAIN + '/success/',
            cancel_url=settings.DOMAIN + '/cancel/',
        )
        # return JsonResponse({'id': checkout_session.id})
        return redirect(checkout_session.url, code=303)


class StripeOrderIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(id=self.kwargs.get('id'))
            intent = stripe.PaymentIntent.create(
                amount=order.total_amount,
                currency=order.items.last().currency,
                payment_method_types=['card'],
                # automatic_payment_methods={
                #     'enabled': True,
                # }
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})


def home_page_view(request):
    items = Item.objects.all()
    orders = Order.objects.all()
    return render(request, 'home.html', {
        'items': items,
        'orders': orders,
    })


class SuccessPageView(TemplateView):
    template_name = 'success.html'


class CancelPageView(TemplateView):
    template_name = 'cancel.html'

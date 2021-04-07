from basketapp.models import Basket


def baskets(request):
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    return {
        'baskets': basket,
    }

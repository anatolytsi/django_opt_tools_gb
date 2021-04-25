from basketapp.models import Basket


def basket(request):
    return {
        "baskets": Basket.objects.filter(user=request.user).select_related() if request.user.is_authenticated else []
    }

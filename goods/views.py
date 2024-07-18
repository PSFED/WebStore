from django.shortcuts import render

from goods.models import Categories, Goods


def category(request):
    category = Categories.objects.all()
    context = {
        "category": category,
    }
    return render(request, context)


def good(request, good_slug):
    good = Goods.objects.filter(slug=good_slug)
    context = {
        "good": good,
    }
    return render(request, context)

from django.shortcuts import render


# Create your views here.

def show_index(request, context=None):
    return render(request, 'index.html', context)

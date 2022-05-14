from django.urls import path

from quotes.views import QuotesView, QuoteCreateView

app_name = 'quotes'
urlpatterns = [
    path('', QuotesView.as_view(), name='quotes'),
    path('create/', QuoteCreateView.as_view(), name='create-quotes'),
]

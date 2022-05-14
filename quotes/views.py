from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, UpdateView, DeleteView
from django.views.generic import CreateView

from quotes.forms import CreateQuoteForm, QuoteSearchForm
from quotes.models import Quotes


class QuotesView(ListView):
    template_name = 'quotes/quotes.html'
    paginate_by = 10

    def get_queryset(self, **kwargs):
        return Quotes.objects.select_related(
            "user_id"
        ).prefetch_related(
            "tag"
        ).order_by("-id")


class QuoteMixin:
    model = Quotes
    fields = '__all__'


class QuoteCreateView(QuoteMixin, CreateView):
    template_name = "quotes/create.html"
    success_url = reverse_lazy('quotes:quotes')

    def get_queryset(self, **kwargs):
        return Quotes.objects.prefetch_related(
            "tag"
        ).order_by("-id")


@method_decorator(login_required, name='dispatch')
class QuoteUpdateView(QuoteMixin, UpdateView):
    success_url = reverse_lazy('quotes:quotes')


@method_decorator(login_required, name='dispatch')
class QuoteDeleteView(QuoteMixin, DeleteView):
    success_url = reverse_lazy('quotes:quotes')
# class CreateQuoteView(View):
#     template_name = "quotes/create.html"
#     form = CreateQuoteForm
#
#     def get(self, request):
#         return render(request, template_name=self.template_name, context={"form": self.form})
#
#     def post(self, request):
#         print(request.user)
#         form = self.form(request.POST, user=request.user)
#         form.is_valid()
#         form.save()

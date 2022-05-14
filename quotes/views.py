from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
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


class QuoteCreateView(View):
    template_name = "quotes/create.html"
    form_class = CreateQuoteForm
    success_url = reverse_lazy('quotes:quotes')

    def get_queryset(self, **kwargs):
        return Quotes.objects.prefetch_related(
            "tag"
        ).order_by("-id")

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST, request=request)
        print(form.is_valid())
        print(request.POST)
        if form.is_valid():
            form.clean()
            form.save()
            return redirect("quotes:quotes")
        print(form.errors)
        return render(request, self.template_name, {"form": form})


@method_decorator(login_required, name='dispatch')
class QuoteUpdateView(UpdateView):
    success_url = reverse_lazy('quotes:quotes')


@method_decorator(login_required, name='dispatch')
class QuoteDeleteView(DeleteView):
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

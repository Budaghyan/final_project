from django import forms

from quotes.models import Quotes
from tags.models import Tags


class CreateQuoteForm(forms.ModelForm):
    class Meta:
        model = Quotes
        fields = ['text', 'tag']

    tag = forms.ModelMultipleChoiceField(
        queryset=Tags.objects.all()
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        self.cleaned_data = super().clean()
        self.cleaned_data["user_id"] = self.request.user
        return self.cleaned_data

    def save(self):
        self.instance.user_id = self.request.user
        super(CreateQuoteForm, self).save()

class QuoteSearchForm(forms.Form):
    category = forms.ModelChoiceField(Quotes.objects.order_by('tag'), required=False)


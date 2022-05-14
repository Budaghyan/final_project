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
        super(CreateQuoteForm, self).__init__()
        self.user = None
        if kwargs.get("user"):
            self.user = kwargs["user"]

    def clean(self):
        super().clean()
        print(self.get_context())
        self.cleaned_data["user_id"] = self.user
        return self.cleaned_data

    def save(self, commit=True):
        self.instance.user_id = self.user
        super().save()


class QuoteSearchForm(forms.Form):
    category = forms.ModelChoiceField(Quotes.objects.order_by('tag'), required=False)


from django import forms

from rakuten.models import Rakuten


class RakutenForm(forms.ModelForm):
    class Meta:
        model = Rakuten
        fields = ('title', 'code', 'description')


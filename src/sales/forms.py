from django import forms



CHART_CHOICES = (
  ('#1', 'Bar chart'),
  ('#1', 'Pie chart'),
  ('#3', 'Linear chart'),
)


class SalesSearchForm(forms.Form):
  date_from = forms.DateField(widget=forms.DateInput(attrs={ 'type': 'date' }))
  date_to = forms.DateField(widget=forms.DateInput(attrs={ 'type': 'date' }))
  chart_type = forms.ChoiceField(choices=CHART_CHOICES)

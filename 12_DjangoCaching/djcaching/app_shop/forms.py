from django import forms


class BalanceForm(forms.Form):
    balance = forms.DecimalField(max_digits=10, decimal_places=2)

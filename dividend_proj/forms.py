from django import forms
from .models import Holding


class HoldingForm(forms.ModelForm):
    class Meta:
        model = Holding
        #fields users type in
        fields = ['ticker', 'shares_amnt', 'auto_reinvest']

        labels = {
            'ticker': 'Stock Ticker', 
            'shares_amnt': 'Number of Shares',
            'auto_reinvest': 'Enroll in DRIP?'
            }       
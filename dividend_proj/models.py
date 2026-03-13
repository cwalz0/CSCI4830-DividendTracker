from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class DividendData(models.Model):
    #local storage for 3rd party api
    ticker = models.CharField(max_length=10)
    name = models.CharField(max_length=100, default="Unknown")
    dividend_yield = models.DecimalField(max_digits=7, decimal_places=4, null=True, blank=True)
    dividend_per_share = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)



    #TODO
    payout_frequency = models.CharField(max_length=20, null=True, blank=True) 
    next_payout = models.DateField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True) #tracks last time fetched
    

    class Meta:
        # This tells the Django Admin exactly how to spell the plural version
        verbose_name_plural = "Dividend Data" 

    def __str__(self):
        return f"{self.ticker} Market Data"


class Holding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="holdings")
    ticker = models.CharField(max_length=10)

    # decimalfield instead of float to avoid rounding errors
    shares_amnt = models.DecimalField(max_digits=15, decimal_places=4)
    auto_reinvest = models.BooleanField(default=False)

    #link user's holding to stored api data
    market_data = models.ForeignKey(DividendData, on_delete=models.SET_NULL, null=True, blank=True)


    class Meta:
        unique_together = ('user', 'ticker')

    @property
    def annual_income(self):
        if self.market_data and self.market_data.dividend_per_share:
            return self.shares_amnt * self.market_data.dividend_per_share
        return 0

    def __str__(self):
        return f"{self.user.username} - {self.shares_amnt}x {self.ticker}"
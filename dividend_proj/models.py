from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class DividendData(models.Model):
    #local cache for 3rd party api
    #update after 24hrs
    ticker = models.CharField(max_length=10)
    dividend_yield = models.DecimalField(max_digits=7, decimal_places=4, null=True, blank=True)
    dividend_per_share = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    payout_frequency = models.CharField(max_length=20, null=True, blank=True) # quarterly / monthly
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
    shares = models.DecimalField(max_digits=15, decimal_places=4)
    auto_reinvest = models.BooleanField(default=False)

    #link user's holding to cached api
    market_data = models.ForeignKey(DividendData, on_delete=models.SET_NULL, null=True, blank=True)


    class Meta:
        unique_together = ('user', 'ticker')

    def __str__(self):
        return f"{self.user.username} - {self.shares}x {self.ticker}"
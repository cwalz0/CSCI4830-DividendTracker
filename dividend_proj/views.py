from django.shortcuts import render, redirect
from django.contrib.auth.models import User # temp
#from django.contrib.auth.decorators import login_required
from .models import Holding, DividendData
from .forms import HoldingForm
import yfinance as yf
from decimal import Decimal

# Create your views here.

#login_required only allows viewing if logged in
#otherwise, redirects to the login page

# temporarily removing login for due date
# @login_required
def dashboard(request):
    #just grabbing first user for due date
    #user_holdings = Holding.objects.filter(user=request.user)
    current_user = User.objects.first()

    if request.method == 'POST':
        form = HoldingForm(request.POST)
        if form.is_valid():
            ticker_symbol = form.cleaned_data['ticker'].upper()

            # get / create market data storage for ticker
            market_data, created = DividendData.objects.get_or_create(ticker=ticker_symbol)

            if created:
                stock = yf.Ticker(ticker_symbol)
                div_yield = stock.info.get('dividendYield', 0)
                div_rate = stock.info.get('dividendRate', 0)

                market_data.dividend_yield = Decimal(str(div_yield)) if div_yield else Decimal('0.00')
                market_data.dividend_per_share = Decimal(str(div_rate)) if div_rate else Decimal('0.00')
                market_data.save()


                existing_holding = Holding.objects.filter(user=current_user, ticker=ticker_symbol).first()

                if existing_holding:
                    existing_holding.shares_amnt += form.cleaned_data['shares_amnt']
                    existing_holding.save()
                else:
                    new_holding = form.save(commit=False)
                    new_holding.user = current_user
                    new_holding.market_data = market_data
                    new_holding.save()

            return redirect('dashboard')
    else:
        form = HoldingForm()

    user_holdings = Holding.objects.filter(user=current_user)
        
                

    #pack data into dict

    context = {
        'holdings': user_holdings,
        'form': form,
    }

    return render(request, 'dividend_proj/dashboard.html', context)
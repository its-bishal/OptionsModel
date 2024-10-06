
import streamlit as st  
import pandas as pd
import numpy as np
import sys

from model.BlackScholesModel import BlackScholesModel

st.set_page_config(page_title='Options Pricing', page_icon=':chart_with_upwards_trend:', layout='wide', initial_sidebar_state='auto')
st.title('Options Pricing')

with st.sidebar:
    st.write('Select the model to use for options pricing')
    model = st.selectbox('Model', ['Monte Carlo','Black-Scholes', 'Binomial'])

    st.write('###Input Options Parameters')
    option_type = st.selectbox('Option Type', ('Call', 'Put'))
    spot = st.number_input('Spot Price', value=100.0, min_value=0.01, max_value=1000000.)
    strike = st.number_input('Strike Price', value=110.0, min_value=0.01, max_value=1000000.)

    if option_type == "Call":
        if strike > spot:
            st.write(f"OTM: {round((strike-spot)/spot*100, 2)}%")
        elif strike == spot:
            st.write(f"ATM: 0%")
        else:
            st.write(f"ITM: {round((spot-strike)/spot*100,2)}%")
    else:
        if strike > spot:
            st.write(f"ITM: {round((strike-spot)/spot*100, 2)}%")
        elif strike == spot:
            st.write(f"ATM: 0%")
        else:
            st.write(f"OTM: {round((spot-strike)/spot*100,2)}%")
    
    t = st.slider("Remaining Trading Days", min_value=0, max_value=252, value=22)
    r = st.slider("Interest rate(%)", min_value=0.01, max_value=10., value=2., step=0.01, help='risk-free rate or financing rate')
    sigma = st.slider("Volatility(%)", min_value=0.01, max_value=200., value=30., step=1.)

    st.divider()
    st.write('### Position Settings')
    multiplier = st.number_input('Multiplier', value=1000, min_value=1, max_value=1000000)
    position = st.selectbox('Position', ('Long', 'Short'))
    quantity = st.number_input('Quantity', value=10, min_value=1, max_value=1000000)

st.metric(label="Premium", value=round(BlackScholesModel(spot, strike, t/252, r/100, sigma/100, option_type).premium()))

premium = round(BlackScholesModel(spot, strike, t/252, r/100, sigma/100, option_type).premium())
delta = round(BlackScholesModel(spot, strike, t/252, r/100, sigma/100, option_type).delta())
gamma = round(BlackScholesModel(spot, strike, t/252, r/100, sigma/100, option_type).gamma_one_percent())
theta = round(BlackScholesModel(spot, strike, t/252, r/100, sigma/100, option_type).theta_one_day())
vega = round(BlackScholesModel(spot, strike, t/252, r/100, sigma/100, option_type).vega_one_percent())
rho = round(BlackScholesModel(spot, strike, t/252, r/100, sigma/100, option_type).rho_one_percent())

if position == 'Long':
    quantity = quantity
else:
    quantity = -quantity

def style_negative(v, props=''):
    return props if v < 0 else None

pricing_results = pd.DataFrame(columns=['Premium', 'Delta', 'Gamma(1%)', 'Theta(1%)', 'Vega(1%)', 'Rho(1%)'])
pricing_results['Premium'] = [premium, premium*multiplier*quantity]
pricing_results['Delta'] = [delta, delta*spot*multiplier*quantity]
pricing_results['Gamma(1%)'] = [gamma, gamma*spot*multiplier*quantity]
pricing_results['Theta(1%)'] = [theta, theta*multiplier*quantity]
pricing_results['Vega(1%)'] = [vega, vega*spot*multiplier*quantity]
pricing_results['Rho(1%)'] = [rho, rho*spot*multiplier*quantity]

st.dataframe(pricing_results, use_container_width=True)
st.divider()

st.write(f"Position Matrix")
value_input = st.selectbox('Value of matrix', ('Premium', 'Delta', 'Gamma(1%)', 'Theta(1%)', 'Vega(1%)', 'Rho(1%)'))

price_range = np.arange(spot*0.7, spot*1.3+1, 1)
time_range = np.arange(1, t+1, 1)

pricing_matrix = pd.DataFrame(columns=time_range, index=price_range)

for t in time_range:
    for s in price_range:
        if value_input == 'Premium':
            pricing_matrix.loc[s, t] = int(BlackScholesModel(spot, strike, t/252, r/100, sigma/100, option_type).premium() * multiplier * quantity)
        elif value_input == 'Delta':
            pricing_matrix.loc[s,t] = int(BlackScholesModel(spot, strike, t/252, r/100, sigma/100, option_type).delta() * spot * multiplier * quantity)
        elif value_input == 'Gamma(1%)':
            pricing_matrix.loc[s,t] = int(BlackScholesModel(spot, strike, t/252, r/100, sigma/100, option_type).gamma_one_percent() * spot * multiplier * quantity)
        elif value_input == 'Theta(1%)':
            pricing_matrix.loc[s,t] = int(BlackScholesModel(spot, strike, t/252, r/100, sigma/100, option_type).theta_one_day() * multiplier * quantity)
        elif value_input == 'Vega(1%)':
            pricing_matrix.loc[s,t] = int(BlackScholesModel(spot, strike, t/252, r/100, sigma/100, option_type).vega_one_percent() * multiplier * quantity)
        elif value_input == 'Rho(1%)':
            pricing_matrix.loc[s,t] = int(BlackScholesModel(spot, strike, t/252, r/100, sigma/100, option_type).rho_one_percent() * multiplier * quantity)
        else:
            sys.exit("error! \n Please check input value...")


pricing_matrix= pricing_matrix.sort_index(ascending=False)
st.dataframe(pricing_matrix, use_container_width=True, height=1000)

st.divider()
st.write('### Delta neutral')

hedge_quantity = '{:,.0f}'.format(abs(round(-delta * multiplier * quantity,0)))

if -delta * multiplier * quantity > 0:
    st.info(f"## Buy {hedge_quantity} shares of underlying asset")
else:
    st.info(f"## Sell {hedge_quantity} shares of underlying asset")




import streamlit as st
import pandas as pd
import sys

from model.BlackScholesModel import BlackScholesModel, calculate_implied_volatility

st.set_page_config(page_title='Implied Volatility Calculation', page_icon=':chart_with_upwards_trend:', layout='wide', initial_sidebar_state='auto')
st.title('Implied Volatility Calculation')


with st.sidebar:

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
    if option_type == 'Call' and spot > strike:
        premium_floor = spot - strike
    elif option_type == 'Put' and spot < strike:
        premium_floor = strike - spot
    else:
        premium_floor = 0.01
    premium = st.number_input('Premium', min_value=0.01, max_value=1000000.)
    st.write('Premium input has to be greater than ' + str(round(premium_floor,2)) + ". (option's barrierr condition)")

    st.divider()
    st.write('### Position Settings')
    multiplier = st.number_input('Multiplier', value=1000, min_value=1, max_value=1000000)
    position = st.selectbox('Position', ('Long', 'Short'))
    quantity = st.number_input('Quantity', value=10, min_value=1, max_value=1000000)


# Implied volatility calculation

ImpliedVol = calculate_implied_volatility(spot, strike, t/252, r/100, premium, option_type)
st.metric(label='Implied Volatility', value=str(round(ImpliedVol*100,2))+'%')

premiumVol = round(BlackScholesModel(spot, strike, t/252, r/100, ImpliedVol, option_type).premium())
deltaVol = round(BlackScholesModel(spot, strike, t/252, r/100, ImpliedVol, option_type).delta())
gammaVol = round(BlackScholesModel(spot, strike, t/252, r/100, ImpliedVol, option_type).gamma_one_percent())
thetaVol = round(BlackScholesModel(spot, strike, t/252, r/100, ImpliedVol, option_type).theta_one_day())
vegaVol = round(BlackScholesModel(spot, strike, t/252, r/100, ImpliedVol, option_type).vega_one_percent())
rhoVol = round(BlackScholesModel(spot, strike, t/252, r/100, ImpliedVol, option_type).rho_one_percent())

if position == 'Long':
    quantity = quantity
else:
    quantity = -quantity

def style_negative(v, props=''):
    return props if v < 0 else None

pricing_results = pd.DataFrame(columns=['Premium', 'Delta', 'Gamma(1%)', 'Theta(1%)', 'Vega(1%)', 'Rho(1%)'])
pricing_results['Premium'] = [premiumVol, premiumVol*multiplier*quantity]
pricing_results['Delta'] = [deltaVol, deltaVol*spot*multiplier*quantity]
pricing_results['Gamma(1%)'] = [gammaVol, gammaVol*spot*multiplier*quantity]
pricing_results['Theta(1%)'] = [thetaVol, thetaVol*multiplier*quantity]
pricing_results['Vega(1%)'] = [vegaVol, vegaVol*spot*multiplier*quantity]
pricing_results['Rho(1%)'] = [rhoVol, rhoVol*spot*multiplier*quantity]

st.dataframe(pricing_results, use_container_width=True)
st.divider()


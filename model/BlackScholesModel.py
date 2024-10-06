
import numpy as np
from scipy.stats import norm

# config
TRADING_DAYS = 260 #252
ACCURACY = 0.0001
IV_UP_BOUND = 2.


class BlackScholesModel:

    def __init__(self, s:float, k:float, t:float, r:float, sigma:float, option_type:str):
        """Args:
            s (float): Spot price of an asset
            k (float): Strike price
            t (float): Time to maturity in years
            r (float): Risk-free interest rate
            sigmma (float): Volatility of the asset
        """
        self.s = s
        self.k = k
        self.t = t
        self.r = r
        self.sigma = sigma
        self.option_type = option_type.lower()


    def d1(self):
        # calculate d1 in black-scholes-merten model
        return (np.log(self.s/self.k) + (self.r + self.sigma**2 / 2) * self.t)/(self.sigma * np.sqrt(self.t))
    
    def d2(self):
        # calculate d2 in black-scholes-merten model
        return self.d1() - (self.sigma * np.sqrt(self.t))
    
    def premium(self):
        # calculate the theoretical option price in black-scholes-merten model

        if self.t == 0:
            if self.option_type in ['Call', 'call', 'C', 'c']:
                return max(self.s - self.k, 0)
            elif self.option_type in ['Put', 'put', 'P', 'p']:
                return max(self.k - self.s, 0)
            else:
                raise ValueError('Option type must be either Call or Put')
        else:
            if self.option_type in ['Call', 'call', 'C', 'c']:
                return norm.cdf(self.d1()) * self.s - norm.cdf(self.d2()) * self.k * np.exp(-self.r * self.t)
            elif self.option_type in ['Put', 'put', 'P', 'p']:
                return norm.cdf(-self.d2()) * self.k * np.exp(-self.r * self.t) - norm.cdf(-self.d1()) * self.s
            else:
                raise ValueError('Option type must be either Call or Put')
            
    def delta(self):
        # calculate the delta of the option in black-scholes-merten model
        # delta is the sensitivity of the option price to a change in the price of underlying security
        # if underlying price increases by one unit, by how much does the option price increase
        if self.option_type in ['Call', 'call', 'C', 'c']:
            return norm.cdf(self.d1())
        elif self.option_type in ['Put', 'put', 'P', 'p']:
            return norm.cdf(self.d1()) - 1
        else:
            raise ValueError('Option type must be either Call or Put')
    
    def gamma_one_percent(self):
        # calculate the gamma one percent in black-scholes-merten model, using difference method
        # gamma is the sensitivity of delta with respect to the underlying price
        # call options typically have a positive gamma, while put options usually have negative gamma
        # the impact of one percent underlying price on option's delta

        return BlackScholesModel(self.s*1.005, self.k, self.t, self.r, self.sigma, self.option_type).delta() - \
                BlackScholesModel(self.s*0.995, self.k, self.t, self.r, self.sigma, self.option_type).delta()
    
    def vega_one_percent(self):
        # calculate the vega one percent difference in black-scholes-merten model, using difference method
        # vega is the sensitivity of the option price to a change in the volatility
        # the impact of one percent change in voltility on option's price
        return BlackScholesModel(self.s, self.k, self.t, self.r, self.sigma+0.005, self.option_type).premium() - \
                BlackScholesModel(self.s, self.k, self.t, self.r, self.sigma-0.005, self.option_type).premium()

    def theta_one_day(self):
        # calculate the theta one day in black-scholes-merten model, using difference method
        # theta is the sensitivity of option's price to the passage of time, also called time decay
        # the impact of one day pass in time to maturity on optionprice

        return BlackScholesModel(self.s, self.k, self.t-1/TRADING_DAYS, self.r, self.sigma, self.option_type).premium() - \
                self.premium()

    def rho_one_percent(self):
        # calculate the rho one percent in black-scholes-merten model, using difference method
        #  rho is the sensitivity of the option price to the change in interest rate
        # the impact of one percent change in interest rate on option's price

        return BlackScholesModel(self.s, self.k, self.t, self.r+0.005, self.sigma, self.option_type).premium() - \
                BlackScholesModel(self.s, self.k, self.t, self.r-0.005, self.sigma, self.option_type).premium()



def calculate_implied_volatility(s:float, k:float, t:float, r:float, premium:float, option_type:str):
    # calculate the implied volatility using the black-scholes model
    # given the option's premium, underlying price, strike price, time to maturity, interest rate and option type, calculate the implied volatility
    # the implied volatility is the volatility that makes the black-scholes model price equal to the premium
    # the implied volatility is a measure of the market's expectation of the future volatility of the underlying asset

    accuracy = ACCURACY
    low_bound = ACCURACY
    up_bound = IV_UP_BOUND

    low_premium = BlackScholesModel(s, k, t, r, low_bound, option_type).premium()
    up_premium = BlackScholesModel(s, k, t, r, up_bound, option_type).premium()


    if(low_premium - premium) * (up_premium - premium) < 0:
        while(up_bound - low_bound)/2 >= accuracy:
            mid = (up_bound +  low_bound)/2
            mid_premium = BlackScholesModel(s, k, t, r, mid, option_type).premium()

            if(mid_premium-premium) * (low_premium-premium)<0:
                up_bound = mid
                up_premium = mid_premium
            elif(mid_premium-premium) * (up_premium-premium)<0:
                low_bound = mid
                low_premium = mid_premium
            else:
                up_bound = mid
                low_bound = mid

        ImpVol = (up_bound + low_bound)/2
        return ImpVol
    else:
        raise Exception("error! \n implied volatility is not in the range of 0 to 2. Please check premium input")
    

# if __name__ == '__main__':
#     calculate = BlackScholesModel(s=100, k=105, t=60/252, r=0.02, sigma=0.3, option_type='call')

#     print(f"premium: {calculate.premium()}")
#     print(f"Delta: {calculate.delta()}")
#     print(f"Gamma (one percent): {calculate.gamma_one_percent()}")
#     print(f"Theta (one percent): {calculate.theta_one_day()}")
#     print(f"Vega (one percent): {calculate.vega_one_percent()}")
#     print(f"Rho (one percent): {calculate.rho_one_percent()}")
    
    
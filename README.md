# Options Pricing Model App - Black-Scholes

## Overview

This app is a Python-based web application designed to price European-style options using widely-known method: the **Black-Scholes-Merton model**. The app allows users to input key financial parameters, calculate the price of a European call or put option, and visualize the results in real-time. It is implemented using **NumPy** and **SciPy** for numerical calculations, and **Streamlit** for deployment, along with **Pandas** for data management.

## Features

- **Black-Scholes-Merton Model**:
    - Analytical solution for pricing European call and put options.
    - Implemented using the finite difference method for differential equations.

- **Interactive UI**:
    - Easy-to-use web interface built with Streamlit for entering parameters and calculating option prices.
    - Real-time calculation and visualization of option prices.

## Prerequisites

Before running the app, ensure you have the following libraries installed:

- Python 3.x
- NumPy
- SciPy
- Pandas
- Streamlit

You can install these packages using the following:

```bash
pip install numpy scipy pandas streamlit
```

## Class: `BlackScholesModel`

The `BlackScholesModel` class is the core component of this app. It contains methods for pricing European options using the **Black-Scholes-Merton model**

### Methods

1. **`__init__()`**:  
   Initializes the class with the required parameters:
   - `S`: Spot price of the underlying asset.
   - `K`: Strike price of the option.
   - `T`: Time to expiration (in years).
   - `r`: Risk-free interest rate (annualized).
   - `sigma`: Volatility of the underlying asset.
   - `option_type`: Either 'call' or 'put' to specify option type.

2. **`BlackScholesModel`**:  
   Uses the Black-Scholes-Merton model to calculate the price of a European option. The finite difference method is employed for the solution of partial differential equations (PDEs).


## How to Run the App

1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/options-pricing-app.git
   cd options-pricing-app
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

4. The app will launch in your default web browser. Input the required parameters such as:
   - Spot Price
   - Strike Price
   - Time to Expiration
   - Risk-free Rate
   - Volatility
   - Option Type (Call/Put)

5. View the option price calculated using both Black-Scholes and Monte Carlo methods.

## File Structure

```
options-pricing-app/
│
├── app.py                 # Main file to run the Streamlit application
├── BlackScholesModel.py   # Contains the BlackScholesModel class and methods
├── requirements.txt       # Dependencies required for the project
└── README.md              # Project documentation
```

## Future Improvements

- Add support for American-style options.
- Extend the application with other pricing models (e.g., binomial trees, finite difference methods for PDE).
- Add interactive charts to visualize Monte Carlo simulation paths.
  
---


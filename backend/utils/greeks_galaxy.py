import numpy as np
from scipy.stats import norm
from typing import Dict

def black_scholes_call(S: float, K: float, T: float, r: float, sigma: float) -> float:
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

def black_scholes_put(S: float, K: float, T: float, r: float, sigma: float) -> float:
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

def calculate_delta(S: float, K: float, T: float, r: float, sigma: float, option_type: str = 'call') -> float:
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    if option_type == 'call':
        return norm.cdf(d1)
    else:
        return norm.cdf(d1) - 1

def calculate_gamma(S: float, K: float, T: float, r: float, sigma: float) -> float:
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return norm.pdf(d1) / (S * sigma * np.sqrt(T))

def calculate_theta(S: float, K: float, T: float, r: float, sigma: float, option_type: str = 'call') -> float:
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    theta_call = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) - 
                  r * K * np.exp(-r * T) * norm.cdf(d2))
    
    if option_type == 'call':
        return theta_call / 365
    else:
        theta_put = theta_call + r * K * np.exp(-r * T)
        return theta_put / 365

def calculate_vega(S: float, K: float, T: float, r: float, sigma: float) -> float:
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return S * norm.pdf(d1) * np.sqrt(T) / 100

def calculate_rho(S: float, K: float, T: float, r: float, sigma: float, option_type: str = 'call') -> float:
    d2 = (np.log(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    if option_type == 'call':
        return K * T * np.exp(-r * T) * norm.cdf(d2) / 100
    else:
        return -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100

async def calculate_all_greeks(symbol: str) -> Dict:
    S = 100.0
    K = 100.0
    T = 0.25
    r = 0.05
    sigma = 0.25
    
    return {
        "symbol": symbol,
        "delta_call": calculate_delta(S, K, T, r, sigma, 'call'),
        "delta_put": calculate_delta(S, K, T, r, sigma, 'put'),
        "gamma": calculate_gamma(S, K, T, r, sigma),
        "theta_call": calculate_theta(S, K, T, r, sigma, 'call'),
        "theta_put": calculate_theta(S, K, T, r, sigma, 'put'),
        "vega": calculate_vega(S, K, T, r, sigma),
        "rho_call": calculate_rho(S, K, T, r, sigma, 'call'),
        "rho_put": calculate_rho(S, K, T, r, sigma, 'put')
    }

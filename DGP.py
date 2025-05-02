import numpy as np
import pandas as pd

def DGP_sample(trend: float,
               seasonality: float,
               noise: float,
               num_samples=50,
               trend_function=lambda x, t: x*t,
               seasonality_points=[4,12],
               seasonality_cycle=12,
               start_date='1-1-2000',
               date_interval='ME',
               seasonality_mode='absolute',
               noise_mode='absolute'):
    
    """
    Generates a synthetic time series dataset based on a simplified Data Generating Process (DGP).

    Parameters:
    -----------
    trend : float
        The base value or slope to be used in the trend function.
    
    seasonality : float
        The amplitude of seasonal effects. Can be absolute or relative to trend.
    
    noise : float
        The range of uniform random noise. Can be absolute or relative to trend.
    
    num_samples : int, optional (default=50)
        Number of time points to generate.
    
    trend_function : function, optional (default=lambda x, t: x * t)
        A function to define how trend changes over time.
        Takes two arguments: trend base value (x) and time step (t).
    
    seasonality_points : list of int, optional (default=[12])
        Points within each seasonal cycle where the seasonality effect applies.
        For example, [6, 12] means the effect will appear at cycle positions 6 and 12.
    
    seasonality_cycle : int, optional (default=12)
        The length of the repeating seasonal cycle.
    
    start_date : str, optional (default='1-1-2000')
        The start date for the generated time series.
    
    date_interval : str, optional (default='ME')
        Frequency of the time series ('D' for daily, 'ME' for monthly, etc.).
    
    seasonality_mode : str, optional (default='absolute')
        If 'absolute', seasonality is used as-is.
        If 'relative', seasonality is scaled by the trend at each point.
    
    noise_mode : str, optional (default='absolute')
        If 'absolute', noise is added uniformly as-is.
        If 'relative', noise is scaled by the trend at each point.

    Returns:
    --------
    pd.DataFrame
        A DataFrame with columns:
        - 'date': Timestamp
        - 'trend': trend component
        - 'seasonality': seasonal component
        - 'noise': random noise
        - 'value': final combined value
    """
    
    dates = pd.date_range(start=start_date, freq=date_interval, periods=num_samples)
    trend_array = np.array([trend_function(trend, i+1) for i in range(num_samples)])
    seasonality_array = np.array([seasonality if (i % seasonality_cycle + 1) in seasonality_points else 0 for i in range(num_samples)])
    noise_array = np.random.uniform(-noise, noise, num_samples)

    if seasonality_mode == 'relative':
        seasonality_array *= trend_array
    if noise_mode == 'relative':
        noise_array *= trend_array

    final_array = trend_array + seasonality_array + noise_array
    
    return pd.DataFrame({
        'date': dates,
        'trend': trend_array,
        'seasonality': seasonality_array,
        'noise': noise_array,
        'value': final_array
    })

import numpy as np

def trend_linear(x, t, scale = 2, offset = 0):
    return scale * x * t + offset
def trend_piecewise(x, t, scale = 2, break_point = 20, post_scale = 0.5):
    return scale * x * t if t <= break_point else scale * break_point * x + post_scale * x * (t - break_point)
def trend_exponential(x, t, scale = 1, rate = 0.03):
    return scale * x * np.exp(rate * t)
def trend_logarithmic(x, t, scale = 1):
    return scale * x * np.log(t + 1)
def trend_wave(x, t, scale = 1, amplitude = 1000, frequency = 0.2):
    return scale * x * t + amplitude * np.sin(frequency * t)
def trend_polynomial(x, t, a = 0.1, b = 2, c = 100):
    return a * x * t**2 - b * t + c
def trend_recovery(x, t, a = 0.4, b = -5, c = 50):
    return a * x * t**2 + b * t + c
import numpy as np
from config import *

prices = []
step = 0
stake = STAKE

def rsi(data):
    deltas = np.diff(data)
    gains = deltas.clip(min=0)
    losses = -deltas.clip(max=0)
    avg_gain = np.mean(gains[-RSI_PERIOD:])
    avg_loss = np.mean(losses[-RSI_PERIOD:])
    if avg_loss == 0:
        return 100
    return 100 - (100 / (1 + avg_gain / avg_loss))

def stochastic(data):
    low = min(data[-STOCH_PERIOD:])
    high = max(data[-STOCH_PERIOD:])
    return 100 * (data[-1] - low) / (high - low) if high != low else 50

def bollinger(data):
    sma = np.mean(data[-BB_PERIOD:])
    std = np.std(data[-BB_PERIOD:])
    return sma + BB_STD * std, sma - BB_STD * std

def signal(price):
    prices.append(price)
    if len(prices) < max(RSI_PERIOD, STOCH_PERIOD, BB_PERIOD):
        return None

    if len(prices) > 200:
        prices.pop(0)

    r = rsi(prices)
    s = stochastic(prices)
    upper, lower = bollinger(prices)

    if r <= 30 and s <= 20 and price <= lower:
        return "CALL"

    if r >= 70 and s >= 80 and price >= upper:
        return "PUT"

    return None

def update_stake(win):
    global step, stake

    if win:
        step = 0
        stake = STAKE
    else:
        step += 1
        if step > MAX_STEPS:
            return None
        stake = round(stake * MARTINGALE_MULTIPLIER, 2)

    return stake

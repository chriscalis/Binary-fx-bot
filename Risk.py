daily_loss = 0.0

def update_daily(profit):
    global daily_loss
    if profit < 0:
        daily_loss += abs(profit)
    return daily_loss

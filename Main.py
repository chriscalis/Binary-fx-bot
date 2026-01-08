import time
from deriv_ws import DerivWS
from strategy import signal, update_stake
from risk import update_daily
from config import *

def main():
    client = DerivWS()
    stake = STAKE

    while True:
        try:
            price = client.get_tick(SYMBOL)
            direction = signal(price)

            if not direction:
                time.sleep(CHECK_INTERVAL)
                continue

            print(f"📍 Signal: {direction} | Stake: {stake}")
            profit = client.buy_contract(stake, direction)

            print(f"💰 Trade result: {profit}")
            daily_loss = update_daily(profit)

            if daily_loss >= DAILY_LOSS_LIMIT:
                print("🛑 Daily loss limit reached. Bot stopped.")
                break

            win = profit > 0
            new_stake = update_stake(win)
            if new_stake is None:
                print("🛑 Max martingale reached. Bot stopped.")
                break

            stake = new_stake
            time.sleep(CHECK_INTERVAL)

        except Exception as e:
            print("⚠️ Error:", e)
            time.sleep(5)

if __name__ == "__main__":
    main()

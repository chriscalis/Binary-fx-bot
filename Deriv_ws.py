import websocket, json, os, time

TOKEN = os.getenv("DERIV_TOKEN")
WS_URL = "wss://ws.derivws.com/websockets/v3?app_id=1089"

class DerivWS:
    def __init__(self):
        self.ws = websocket.WebSocket()
        self.ws.connect(WS_URL)
        self.authorize()

    def authorize(self):
        self.ws.send(json.dumps({"authorize": TOKEN}))
        res = json.loads(self.ws.recv())
        if "error" in res:
            raise Exception("Authorization failed")
        print("✅ Authorized")

    def get_tick(self, symbol="R_75"):
        self.ws.send(json.dumps({"ticks": symbol, "subscribe": 0}))
        return float(json.loads(self.ws.recv())["tick"]["quote"])

    def buy_contract(self, stake, contract_type):
        payload = {
            "buy": 1,
            "price": stake,
            "parameters": {
                "amount": stake,
                "basis": "stake",
                "contract_type": contract_type,
                "currency": "USD",
                "symbol": "R_75",
                "duration": 5,
                "duration_unit": "t"
            }
        }
        self.ws.send(json.dumps(payload))
        buy_res = json.loads(self.ws.recv())

        contract_id = buy_res["buy"]["contract_id"]

        # Subscribe to result
        self.ws.send(json.dumps({
            "proposal_open_contract": 1,
            "contract_id": contract_id
        }))

        while True:
            res = json.loads(self.ws.recv())
            if res["proposal_open_contract"]["is_sold"]:
                profit = res["proposal_open_contract"]["profit"]
                return profit

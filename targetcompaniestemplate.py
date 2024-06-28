import json

qm500 = {}

APPLE_TEMPLATE = '{ "ticker":"AAPL", "prevPrice": 0, "currPrice": 1 }'
APPLE = json.loads(APPLE_TEMPLATE)

qm500["Apple"] = APPLE

print(qm500)
print(qm500["Apple"]["ticker"])


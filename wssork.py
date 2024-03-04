import json

from websocket import create_connection


class websocket:
    def __init__(self, address):
        self.ws = create_connection(address)

    def send(self, params):
        self.ws.send(json.dumps(params))
        result = self.ws.recv()
        return result


address = 'ws://47.107.232.149:8087/wss/mj?devSn=111111202207272'
params = {
    "cmd": "register",
    "headers":
        {
            "req_id": "123451"
        },
    "body":
        {
            "nonce": 123451,
            "timestamp": 1231231,
            "sn": "111111202207272"
        }
}
params1={
   "cmd":"active",
   "headers":
	{
		"req_id":"123451"
	},
	"body":
	{
		"active_code":"xxxx"
	}
}

params2={
   "cmd":"subscribe_corp",
   "headers":
	{
		"req_id":"123451"
	},
	"body":
	{
		"secret":"xxxxx",
		"firmware_version":"xxxxx"
	}
}



web = websocket(address)
# print(type(web))
result1 = json.loads(web.send(params))
print(result1['body']['active_code'])
code=result1['body']['active_code']
params1['body']['active_code']=code
print(params1)
#设备激活
result11 = json.loads(web.send(params1))
secret=result11['body']['secret']
params2['body']['secret']=secret
print(result11)
print(params2)
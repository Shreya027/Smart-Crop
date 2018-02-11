import http.client

conn = http.client.HTTPConnection("api.msg91.com")

payload = "{ \"sender\": \"SOCKET\", \"route\": \"4\", \"country\": \"91\", \"sms\": [ { \"message\": \"Message1\", \"to\": [ \"9769953291\"] }] }"


headers = {
    'authkey': "197517AZ3pT96i9Ef05a7e37ef",
    'content-type': "application/json"
}

conn.request("POST", "/api/v2/sendsms", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

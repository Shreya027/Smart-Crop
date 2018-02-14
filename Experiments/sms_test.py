import http.client

conn = http.client.HTTPConnection("api.msg91.com")

payload = "{ \"sender\": \"SOCKET\", \"route\": \"4\", \"country\": \"91\", \"sms\": [ { \"message\": \"Heavy Rainfall (cloudburst) alert in Chindwara region. Kindly stay indoors until further notice\", \"to\": [ \"9769953291\",\"9819515144\",\"7738554209\"] }] }"


headers = {
    'authkey': "197517AZ3pT96i9Ef05a7e37ef",
    'content-type': "application/json"
}

conn.request("POST", "/api/v2/sendsms", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

import requests

#TODO get auth token
headers = {
    'Host': 'api.myorbit.id',
    'X-Localization': 'id',
    'Sec-Ch-Ua-Mobile': '?0',
    'Authorization': 'Bearer REDACTED',
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
    'Channel': 'web',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'X-Api-Key': 'REDACTED',
    'Sec-Ch-Ua': '"(Not(A:Brand";v="8", "Chromium";v="101"',
    'Origin': 'https://www.myorbit.id',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.myorbit.id/',
    # 'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
}

params = {
    'msisdn': 'REDACTED',
}

response = requests.get('https://api.myorbit.id/subscription/v1/subscriptions/quota', params=params, headers=headers, verify=None)
quotas = response.json()["data"]["quota"]["data"]
total_quota = 0
for quota in quotas:
    total_quota += int(quota["quota_value"])
'''
TODO: add MB
 t.calculateQuotaValue = function(e) {
            try {
                if (!e)
                    return "0GB";
                var t = e < 1048576
                  , r = t ? e / 1024 : e / 1048576;
                return 0 === r % 1 ? ~~r + " " + (t ? "MB" : "GB") : r.toFixed(1) + " " + (t ? "MB" : "GB")
            } catch (n) {
                return "0GB"
            }
        }
'''
print("Remanining quota: {} GB".format(total_quota/(1<<20)))
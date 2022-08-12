import requests
import generator
from urllib.parse import urlparse, parse_qs

headers1 = {
    'Host': 'ciam.myorbit.id:10001',
    # 'Content-Length': '2',
    'Sec-Ch-Ua': '"(Not(A:Brand";v="8", "Chromium";v="101"',
    'Am-Mail': 'REDACTED',
    'Sec-Ch-Ua-Mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
    'Content-Type': 'application/json;charset=UTF-8',
    'Accept': 'application/json, text/plain, */*',
    'Am-Clientid': 'REDACTED',
    'Am-Password': 'REDACTED',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Origin': 'https://www.myorbit.id',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.myorbit.id/',
    # 'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
}

params1 = {
    'authIndexType': 'service',
    'authIndexValue': 'emailLogin',
}

response = requests.post('https://ciam.myorbit.id:10001/iam/v1/realms/tsel/authenticate', params=params1, headers=headers1, json={}, verify=None)
if response.status_code != 200:
    print("invalid email")
    exit(1)

tokenId = response.json()['tokenId']
cookies = {
    'iPlanetDirectoryPro': tokenId,
}

headers2 = {
    'Host': 'ciam.myorbit.id:10001',
    'Sec-Ch-Ua': '"(Not(A:Brand";v="8", "Chromium";v="101"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://www.myorbit.id/',
    # 'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
}

code_verifier = generator.code_verifier()
code_challenge = generator.code_challenge(code_verifier)
params2 = {
    'client_id':'REDACTED',
    'redirect_uri': 'https://www.myorbit.id/callback',
    'response_type': 'code',
    'nonce': 'true',
    'scope': 'profile openid',
    'csrf': tokenId,
    'code_challenge': code_challenge,
    'code_challenge_method': 'S256',
}
response = requests.get('https://ciam.myorbit.id:10001/iam/v1/oauth2/realms/tsel/authorize', cookies=cookies, headers=headers2, params=params2, verify=None)
if response.status_code != 403:
    exit("cannot get callback code")

callback_location = urlparse(response.url)
callback_code = parse_qs(callback_location.query)['code'][0]

headers = {
    'Host': 'ciam.myorbit.id:10001',
    # 'Content-Length': '2',
    'Sec-Ch-Ua': '"(Not(A:Brand";v="8", "Chromium";v="101"',
    'Code': 'REDACTED',
    'Sec-Ch-Ua-Mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json, text/plain, */*',
    'Email': 'kalisokolor@yahoo.com',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Origin': 'https://www.myorbit.id',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.myorbit.id/',
    # 'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
}

data = '{}'
response = requests.post('https://ciam.myorbit.id:10001/iam/v1/oauth2/realms/tsel/access_token?grant_type=authorization_code&redirect_uri=https://www.myorbit.id/callback&code=REDACTED&client_id=REDACTED&client_secret=REDACTED&code_verifier=REDACTED', headers=headers, data='{}', verify=None)

if response.status_code != 200:
    exit("failed to get csrf token")

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
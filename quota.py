import requests
import generator
import os
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs

base_header = {
    'Host': 'ciam.myorbit.id:10001',
    'Sec-Ch-Ua': '"(Not(A:Brand";v="8", "Chromium";v="101"',
    'Sec-Ch-Ua-Mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
    'Content-Type': 'application/json;charset=UTF-8',
    'Accept': 'application/json, text/plain, */*',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Origin': 'https://www.myorbit.id',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.myorbit.id/',
    'Accept-Language': 'en-US,en;q=0.9',
}


def get_token_id():
    response = requests.post('https://ciam.myorbit.id:10001/iam/v1/realms/tsel/authenticate',
                             params={
                                 'authIndexType': 'service',
                                 'authIndexValue': 'emailLogin',
                             },
                             headers=base_header.update({
                                 'Am-Mail': os.getenv("CLIENT_EMAIL"),
                                 'Am-Clientid': os.getenv("CLIENT_AM_ID"),
                                 'Am-Password': os.getenv("CLIENT_PASSWORD"),
                             }),
                             json={},
                             verify=None,
                             )

    if response.status_code != 200:
        exit("invalid email")

    return response


def get_callback_code(code_verifier: str, tokenId: str):
    code_challenge = generator.code_challenge(code_verifier)
    response = requests.get('https://ciam.myorbit.id:10001/iam/v1/oauth2/realms/tsel/authorize',
                            cookies={
                                'iPlanetDirectoryPro': tokenId,
                            },
                            headers=base_header.update({
                                'Sec-Ch-Ua-Platform': '"Windows"',
                                'Upgrade-Insecure-Requests': '1',
                                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                                'Sec-Fetch-Mode': 'navigate',
                                'Sec-Fetch-Dest': 'document',
                                'Referer': 'https://www.myorbit.id/',
                            }),
                            params={
                                'client_id': os.getenv("CLIENT_AM_ID"),
                                'redirect_uri': 'https://www.myorbit.id/callback',
                                'response_type': 'code',
                                'nonce': 'true',
                                'scope': 'profile openid',
                                'csrf': tokenId,
                                'code_challenge': code_challenge,
                                'code_challenge_method': 'S256',
                            },
                            verify=None,
                            )
    if response.status_code != 403:
        exit("cannot get callback code")

    callback_location = urlparse(response.url)
    return parse_qs(callback_location.query)['code'][0]


def get_access_token(callback_code: str, code_verifier: str):
    response = requests.post('https://ciam.myorbit.id:10001/iam/v1/oauth2/realms/tsel/access_token',
                             headers=base_header.update({
                                 'Code': callback_code,
                                 'Content-Type': 'application/x-www-form-urlencoded',
                                 'Email': os.getenv("CLIENT_EMAIL"),
                             }),
                             params={
                                 'grant_type': 'authorization_code',
                                 'redirect_uri': 'https://www.myorbit.id/callback',
                                 'code': callback_code,
                                 'client_id': os.getenv("CLIENT_AM_ID"),
                                 'client_secret': os.getenv("CLIENT_AM_SECRET"),
                                 'code_verifier': code_verifier,
                             },
                             data='{}',
                             verify=None,
                             )
    if response.status_code != 200:
        exit("cannot get access token")

    return response.json()['access_token']


def get_remaining_total_quota(access_token: str):
    response = requests.get('https://api.myorbit.id/subscription/v1/subscriptions/quota',
                            params={
                                'msisdn': os.getenv("MSISDN"),
                            },
                            headers=base_header.update({
                                {
                                    'Authorization': 'Bearer '+access_token,
                                    'X-Api-Key': os.getenv("API_KEY"),
                                }
                            }),
                            verify=None,
                            )
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
    print("Remanining quota: {} GB".format(total_quota/(1 << 20)))


def main():
    tokenId = get_token_id()
    code_verifier = generator.code_verifier()
    callback_code = get_callback_code(tokenId, code_verifier)
    access_token = get_access_token(callback_code, code_verifier)
    get_remaining_total_quota(access_token)


if __name__ == "__main__":
    load_dotenv()
    main()

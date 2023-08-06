import requests, json

class CloudFlareKV:

    def __init__(self, cloudflare_email, auth_key, account_id, namespace_id):
        self.url = "https://api.cloudflare.com/client/v4/accounts/{}/storage/kv/namespaces/{}/values/".format(
            account_id,
            namespace_id
        )
        self.headers = {
            "X-Auth-Email": cloudflare_email,
            "X-Auth-Key": auth_key
        }

    def set(self, key, value):
        url = self.url + key
        return requests.put(url, data=value, headers=self.headers)

    def get(self, key, as_json=False):
        url = self.url + key
        res = requests.get(url, headers=self.headers)
        if res.ok:
            if as_json:
                return json.loads(res.content)
            return res.content

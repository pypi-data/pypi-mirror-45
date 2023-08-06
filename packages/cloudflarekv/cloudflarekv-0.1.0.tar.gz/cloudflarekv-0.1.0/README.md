# cloudflarekv

Super simple access to cloudflare workers kv store

[![PyPI version](https://badge.fury.io/py/cloudflarekv.svg)](https://badge.fury.io/py/cloudflarekv)

## Install

`pip install cloudflarekv`

## Usage

```python
from cloudflarekv.kv import CloudFlareKV
kv = CloudFlareKV(cloudflare_email, auth_key, account_id, namespace_id)
kv.set("foo", "bar")
kv.get("foo")

kv.set("foo-json", '{"foo":"bar"}')
kv.get("foo-json", as_json=True)
```


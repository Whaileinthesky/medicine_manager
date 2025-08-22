import ssl, requests, urllib3
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

# 1) TLS 컨텍스트 구성
ctx = ssl.create_default_context()
ctx.minimum_version = ssl.TLSVersion.TLSv1_2
ctx.maximum_version = ssl.TLSVersion.TLSv1_2
try:
    ctx.set_alpn_protocols(["http/1.1"])   # 일부 환경에선 NotImplementedError 가능
except NotImplementedError:
    pass
ctx.set_ciphers("ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384")

# 2) HTTPAdapter 서브클래싱: PoolManager/ProxyManager에 ssl_context 전달
class TLSAdapter(HTTPAdapter):
    def __init__(self, ssl_context=None, **kwargs):
        self._ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):
        if self._ssl_context is not None:
            pool_kwargs["ssl_context"] = self._ssl_context
        self.poolmanager = urllib3.PoolManager(
            num_pools=connections, maxsize=maxsize, block=block, **pool_kwargs
        )

    def proxy_manager_for(self, proxy, **proxy_kwargs):
        if self._ssl_context is not None:
            # HTTPS 프록시 경로에도 TLS 컨텍스트 적용
            proxy_kwargs["ssl_context"] = self._ssl_context
        return super().proxy_manager_for(proxy, **proxy_kwargs)

# 3) 세션에 장착 + 재시도 정책
retries = Retry(total=3, backoff_factor=0.3, status_forcelist=[502, 503, 504])
s = requests.Session()
s.mount("https://", TLSAdapter(ssl_context=ctx, max_retries=retries))

# 4) 요청
r = s.get("https://apis.data.go.kr/", timeout=10)
print(r.status_code)

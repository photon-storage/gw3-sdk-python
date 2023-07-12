import requests
import base64
import hmac
import hashlib
import time
from urllib.parse import urlparse, parse_qsl,urlencode,urlunparse

ENDPOINT = "https://gw3.io"
EMPTY_DAG_ROOT = "QmUNLLsPACCz1vLxQVkXqqLX5R1X345qqfHbsf67hvA3Nn"


class GW3Client:
    def __init__(self, access_key, access_secret):
        self.access_key = access_key
        self.access_secret = base64.urlsafe_b64decode(access_secret)

    def sign(self, r: requests.PreparedRequest):
        url = urlparse(r.url)
        query = dict(parse_qsl(url.query))
        query["ts"] = str(int(time.time()))
        query = urlencode(query, doseq=True)

        data = f"{r.method}\n{url.path}\n{query}".encode("utf-8")
        mac = hmac.new(self.access_secret, data, hashlib.sha256)
        sign = base64.urlsafe_b64encode(mac.digest())


        r.url = urlunparse(url._replace(query=query))
        r.headers["X-Access-Key"] = self.access_key
        r.headers["X-Access-Signature"] = sign.decode("utf-8")

        return r

    def get_ipfs(self, hash):
        url = f"{ENDPOINT}/ipfs/{hash}"
        req = requests.Request("GET", url)
        prepped = self.sign(req.prepare())

        response = requests.Session().send(prepped)
        if response.ok:
            return response.content

    def get_ipns(self, name):
        url = f"{ENDPOINT}/ipns/{name}"
        req = requests.Request("GET", url)
        prepped = self.sign(req.prepare())

        response = requests.Session().send(prepped)
        if response.ok:
            return response.content

    def auth_upload(self, size):
        url = f"{ENDPOINT}/ipfs/?size={size}"
        req = requests.Request("POST", url)
        prepped = self.sign(req.prepare())

        response = requests.Session().send(prepped)
        if response.ok:
            return response.json()["data"]["url"]

    def upload(self, data):
        url = self.auth_upload(len(data))
        response = requests.post(url, data=data)
        if response.ok:
            return response.headers["IPFS-Hash"]

    def auth_dag_add(self, root, path, size):
        url = f"{ENDPOINT}/ipfs/{root}{path}?size={size}"
        req = requests.Request("PUT", url)
        prepped = self.sign(req.prepare())

        response = requests.Session().send(prepped)
        if response.ok:
            return response.json()["data"]["url"]

    def dag_add(self, root, path, data):
        url = self.auth_dag_add(root, path, len(data))
        response = requests.put(url, data=data)
        if response.ok:
            return response.headers["IPFS-Hash"]

    def auth_dag_rm(self, root, path):
        url = f"{ENDPOINT}/ipfs/{root}{path}"
        req = requests.Request("DELETE", url)
        prepped = self.sign(req.prepare())

        response = requests.Session().send(prepped)
        if response.ok:
            return response.json()["data"]["url"]

    def dag_rm(self, root, path):
        url = self.auth_dag_rm(root, path)
        response = requests.delete(url)
        if response.ok:
            return response.headers["IPFS-Hash"]

    def pin(self, cid):
        url = f"{ENDPOINT}/api/v0/pin/add?arg={cid}"
        req = requests.Request("POST", url)
        prepped = self.sign(req.prepare())

        response = requests.Session().send(prepped)
        if response.ok:
            return response.json()["msg"]

    def unpin(self, cid):
        url = f"{ENDPOINT}/api/v0/pin/rm?arg={cid}"
        req = requests.Request("POST", url)
        prepped = self.sign(req.prepare())

        response = requests.Session().send(prepped)
        if response.ok:
            return response.json()["msg"]

    def create_ipns(self, cid):
        url = f"{ENDPOINT}/api/v0/name/create?arg={cid}"
        req = requests.Request("POST", url)
        prepped = self.sign(req.prepare())

        response = requests.Session().send(prepped)
        if response.ok:
            return response.json()["data"]["name"]

    def update_ipns(self, name, cid):
        url = f"{ENDPOINT}/api/v0/name/publish?arg={cid}&key={name}"
        req = requests.Request("POST", url)
        prepped = self.sign(req.prepare())

        response = requests.Session().send(prepped)
        if response.ok:
            return response.json()["msg"]
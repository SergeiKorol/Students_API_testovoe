
class BaseClient:
    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url

    def request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        return self.session.request(method, url, **kwargs)

    def get(self, path):
        return self.request("GET", path)

    def post(self, path):
        return self.request("POST", path)

    def put(self, path):
        return self.request("PUT", path)

    def delete(self, path):
        return self.request("DELETE", path)






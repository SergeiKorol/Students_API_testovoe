import logging

# Общий лог HTTP для Allure attach
HTTP_LOG = "api.client"
logger = logging.getLogger(HTTP_LOG)


class BaseClient:
    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url

    def request(self, method, path, **kwargs):
        url = f"{self.base_url.rstrip('/')}{path}"
        body = kwargs.get("json")
        logger.info("%s %s | body=%s", method, url, body)
        response = self.session.request(method, url, **kwargs)
        logger.info("<= %s | %s", response.status_code, response.text)
        return response

    def get(self, path, **kwargs):
        return self.request("GET", path, **kwargs)

    def post(self, path, **kwargs):
        return self.request("POST", path, **kwargs)

    def put(self, path, **kwargs):
        return self.request("PUT", path, **kwargs)

    def delete(self, path, **kwargs):
        return self.request("DELETE", path, **kwargs)

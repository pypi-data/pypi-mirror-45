import json

from falcon import HTTPNotFound


class Resource:
    storage = {}

    def on_get(self, req, resp, **kwargs):
        raise HTTPNotFound

    def on_post(self, req, resp, **kwargs):
        raise HTTPNotFound

    def on_put(self, req, resp, **kwargs):
        raise HTTPNotFound

    def on_delete(self, req, resp, **kwargs):
        raise HTTPNotFound


class JSONResource(Resource):
    def json_from_req(self, req):
        if req.content_length:
            try:
                return json.load(req.stream)
            except json.JSONDecodeError:
                return {}
        return {}

    def on_get(self, req, resp, **kwargs):
        self.get(req, resp, **kwargs)

    def get(self, req, resp, **kwargs):
        raise HTTPNotFound

    def on_post(self, req, resp, **kwargs):
        self.post(req, resp, self.json_from_req(req), **kwargs)

    def post(self, req, resp, data, **kwargs):
        raise HTTPNotFound

    def on_put(self, req, resp, **kwargs):
        self.put(req, resp, self.json_from_req(req), **kwargs)

    def put(self, req, resp, data, **kwargs):
        raise HTTPNotFound

    def on_delete(self, req, resp, **kwargs):
        self.delete(req, resp, self.json_from_req(req), **kwargs)

    def delete(self, req, resp, data, **kwargs):
        raise HTTPNotFound

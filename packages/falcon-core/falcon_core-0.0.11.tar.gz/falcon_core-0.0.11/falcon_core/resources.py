import json

import falcon


class Resource:
    use_token = False
    storage = {}

    def json_load_from_req_stream(self, req):
        try:
            if req.content_length:
                data = json.load(req.stream)
            else:
                data = {}
            return data
        except json.JSONDecodeError:
            raise falcon.HTTPBadRequest

    def on_get(self, req, resp, **kwargs):
        self.get(req, resp, **kwargs)

    def get(self, req, resp, **kwargs):
        resp.status = falcon.HTTP_NOT_FOUND

    def on_post(self, req, resp, **kwargs):
        self.post(req, resp, self.json_load_from_req_stream(req), **kwargs)

    def post(self, req, resp, data, **kwargs):
        resp.status = falcon.HTTP_NOT_FOUND

    def on_put(self, req, resp, **kwargs):
        self.put(req, resp, self.json_load_from_req_stream(req), **kwargs)

    def put(self, req, resp, data, **kwargs):
        resp.status = falcon.HTTP_NOT_FOUND

    def on_delete(self, req, resp, **kwargs):
        self.delete(req, resp, self.json_load_from_req_stream(req), **kwargs)

    def delete(self, req, resp, data, **kwargs):
        resp.status = falcon.HTTP_NOT_FOUND

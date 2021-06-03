import json
from rest_framework.renderers import JSONRenderer


class OrganizationJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return json.dumps({'organization_data': data}, ensure_ascii=False)


class DomainJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return json.dumps({'domain_data': data}, ensure_ascii=False)


class SubdomainJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return json.dumps({'subdomain_data': data}, ensure_ascii=False)
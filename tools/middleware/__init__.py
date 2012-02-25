from tools.middleware.jinja import JinjaTemplateResponse


class JinjaMiddleware(object):
    def process_template_response(self, request, response):
        return JinjaTemplateResponse(
            request, response.template_name, response.context_data, 
            content_type=response['Content-Type'],
            status=response.status_code,
        )
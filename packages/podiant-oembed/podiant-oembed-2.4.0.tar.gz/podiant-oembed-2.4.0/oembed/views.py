from django.views.generic.base import View
from django.http.response import HttpResponse
from .models import Resource
from .response import OEmbedResponse
from . import discovery
import re


CONTROL_CHARACTERS = re.compile(
    '[%s]' % re.escape(
        ''.join(map(chr, range(0, 32)))
    )
)


def p(s):
    return s and CONTROL_CHARACTERS.sub('', s) or ''


class OEmbedProviderView(View):
    def get(self, request):
        url = request.GET.get('url')
        if url:
            url = p(url.strip())
            response = discovery.discover(url)

            if response:
                return response

        return HttpResponse(
            '{"error": "Resource not found"}',
            content_type='application/json',
            status=404
        )


class OEmbedAJAXView(View):
    def get(self, request):
        url = request.GET.get('url')
        callback = request.GET.get('callback')

        if url:
            url = p(url.strip())
            response = discovery.discover(url)

            if response is None:
                resource = Resource.load(url)

                response = OEmbedResponse(
                    width=resource.width,
                    height='auto',
                    kind='video',
                    title=resource.title,
                    html=resource.to_html()
                )

            if callback:
                response = response.jsonp(callback)

            return response

        return HttpResponse(
            '{"error": "URL not specified"}',
            content_type='application/json',
            status=404
        )

from django.conf import settings
from django.shortcuts import redirect


def CoverPageMiddleware(get_response):
    def middleware(request):
        # get settings
        config = getattr(settings, 'WEBSITE_COVERPAGE', {})
        active = config.get('active', True)
        url = config.get('url', '/coverpage/')
        cookiename = config.get('cookiename', 'coverpage')

        # do redirect if applicable
        if active and \
           request.method == 'GET' and \
           request.path != url and \
           cookiename not in request.COOKIES:
            return redirect(url)

        # return response
        response = get_response(request)
        return response

    return middleware

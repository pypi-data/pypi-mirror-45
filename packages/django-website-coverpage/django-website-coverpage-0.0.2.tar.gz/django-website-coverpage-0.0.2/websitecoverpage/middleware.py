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
           cookiename not in request.COOKIES and \
           request.method == 'GET' and \
           not request.is_ajax() and \
           request.path != url:

                # check urls to ignore
                do_redirect = True
                ignore_urls = config.get('ignore_urls', [])
                for ig in ignore_urls:
                    if request.path.startswith(ig):
                        do_redirect = False
                        break

                if do_redirect:
                    return redirect(url)

        # return response
        response = get_response(request)
        return response

    return middleware

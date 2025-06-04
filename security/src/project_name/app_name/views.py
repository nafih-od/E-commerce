from http.client import responses

from django.shortcuts import render, redirect
from django.template.defaultfilters import title
from .models import HttpLog
from .models import CmsLog
from .models import DtLog

from .models import NsLog
from .models import CvLog
from app_name.utils import ping
from django.shortcuts import render
from app_name.utils import ssl_info
from app_name.utils import check_ssllabs
from app_name.utils import detect_cms_with_whatweb
from app_name.utils import ns_lookup
from app_name.utils import detect_waf_and_cloudflare
from app_name.utils import cve_lookup_tech




from app_name.utils import check_http_security_headers



from app_name.models import PrintClass, PingsLog,SslLog,SsllabsLog,CmsLog,NsLog

# from django.http import HttpResponseRedirect
#
#
# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt



# def index(request):
#         print_instance = PrintClass.objects.all()
#         context = {
#            "app_title": "Home",
#            "print_instance": _print_instance,
#        }
#         return render(request, 'index.html', context)


def printfun(request):
    response = pings(request)
    response = ssl_view(request)
    response = http_view(request)
    response = ssllabs_view(request)
    response = cms_view(request)
    response = ns_view(request)
    response = detect_view(request)
    response = cvm_view(request)



    _Van = PrintClass.objects.all()
    context = {
        "app_title" : _Van
    }
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            PrintClass.objects.create(name=name)
    return render(request,"index.html",context)


    # context = {
    #    "app_title": "Now",
    #     "print_instance": _print_instance,
    #     "form": _form,
    #     "is_home": True,
    # }
    # return render(request, 'printfun.html', context)




def pings(request):
    if request.method == "POST":
        out = request.POST.get("host")
        if out:
            PingsLog.objects.create(host=out)
            res = ping(out)
            print("result: : : ", res)
        return redirect("app_name:pings")
    return render(request,"index.html")


def ssl_view(request):
    mes= SslLog.objects.all()
    if request.method == "POST":
        dm = request.POST.get("domain")
        if dm:
            SslLog.objects.create(domain=dm)
            mes = ssl_info(dm)
            print("result: : : ", dm)
        return redirect("app_name:ssl_view")
    return render(request, "index.html")


def http_view(request):
    les= HttpLog.objects.all()
    if request.method == "POST":
        lm = request.POST.get("domain")
        if lm:
            HttpLog.objects.create(domain=lm)
            les = check_http_security_headers(lm)
            print("result: : : ", lm)
        return redirect("app_name:http_view")
    return render(request, "index.html")


def ssllabs_view(request):
    aes= SsllabsLog.objects.all()
    if request.method == "POST":
        im = request.POST.get("domain")
        if im:
            SsllabsLog.objects.create(domain=im)
            aes = check_ssllabs(im)
            print("result: : : ", im)
        return redirect("app_name:ssllabs_view")
    return render(request, "index.html")


def cms_view(request):
    bes= CmsLog.objects.all()
    if request.method == "POST":
        op = request.POST.get("domain")
        if op:
            CmsLog.objects.create(domain=op)
            bes = detect_cms_with_whatweb(op)
            print("result: : : ", op)
        return redirect("app_name:cms_view")
    return render(request, "index.html")


def ns_view(request):
    ces= NsLog.objects.all()
    if request.method == "POST":
        lp = request.POST.get("domain")
        if lp:
            NsLog.objects.create(domain=lp)
            bes = ns_lookup(lp)
            print("result: : : ", lp)
        return redirect("app_name:ns_view")
    return render(request, "index.html")


def detect_view(request):
    des= DtLog.objects.all()
    if request.method == "POST":
        mp = request.POST.get("domain")
        if mp:
            DtLog.objects.create(domain=mp)
            des = detect_waf_and_cloudflare(mp)
            print("result: : : ", mp)
        return redirect("app_name:detect_view")
    return render(request, "index.html")


def cvm_view(request):
    kes= CvLog.objects.all()
    if request.method == "POST":
        zp = request.POST.get("domain")
        if zp:
            CvLog.objects.create(domain=zp)
            kes = cve_lookup_tech(zp)
            print("result: : : ", zp)
        return redirect("app_name:cvm_view")
    return render(request, "index.html")

















from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_exempt
import string, random 
from shorter.models import URL
import redis

rds = redis.Redis(host='localhost', port=6379, db=0)


# Create your views here.

def home(request):
    current_site = get_current_site(request)
    return HttpResponse("<h1>Url Shorter</h1>")


def shortit(original_url):

    N = 12 #random hash len
    s = string.ascii_uppercase + string.ascii_lowercase + string.digits

    url_id = ''.join(random.choices(s, k=N))
   
    if not URL.objects.filter(hash=url_id).exists():
        create = URL.objects.create(full_url=original_url, hash=url_id)
        return url_id
    else:
        shortit(url) #generates new hash if already in DB


@csrf_exempt
def generate_short_url(request):
    original_url = request.POST.get("url")
    hash = shortit(original_url)
    current_site = get_current_site(request)
    data = {
        "success": True,
        "id": hash,
        "link": "http://{}/{}".format(current_site, hash),
        "original_url": original_url
    }
    return JsonResponse(data)



def expand_short_url(request,hash_id=None):
    # get the value from redis key, if value not in return None
    hash_code = rds.get(hash_id)
    if hash_code is not None:
        return redirect(hash_code.decode('ascii'))

    if URL.objects.filter(hash=hash_id).exists():
        url = URL.objects.get(hash=hash_id)
        # set the value in redis for faster access
        rds.set(hash_id,url.full_url)
        # redirect the page to the respective url
        return redirect(url.full_url)
    else:
        # if the give key not in redis and db
        return JsonResponse({"success":False})
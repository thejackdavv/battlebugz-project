from django.core.cache import cache
from .models import Bug

CACHE_KEY = "bugs_count"
CACHE_TIMEOUT = 60  # seconds

def bug_count(request):
    count = cache.get(CACHE_KEY)

    if count is None:
        count = Bug.objects.count()
        cache.set(CACHE_KEY, count, CACHE_TIMEOUT)

    return {
        "bugs_count": count
    }
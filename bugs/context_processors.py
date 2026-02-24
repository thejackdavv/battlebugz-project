from bugs.models import Bug


def bug_count(request):
    return {'bugs_count': Bug.objects.count()}
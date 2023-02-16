from .models import Settings
def site(request):
    system_obj = Settings.objects.all()[0]
    return {'site_obj':system_obj}
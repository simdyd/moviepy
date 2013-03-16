from django.conf import settings
from django.contrib.sites.models import Site
#from users_info.models import UserInfo
from film.models import Movie

def movie_vars(request):
    curr_site = Site.objects.get_current();
    #user_info = None
    MOVIE_NO_PICS=Movie.objects.filter(foto=None).count()
    MOVIE_NO_ORI=Movie.objects.filter(video_file=None).count()
    MEDIA_PATH_SITE_REPOSITORY = settings.MEDIA_PATH_SITE_REPOSITORY
    MEDIA_URL_SITE_REPOSITORY = settings.MEDIA_URL
    PREVIEW_URL = settings.PREVIEW_URL
    SITE_TITLE = None 
    SITE_NAME = None
    SITE_TEMPLATE_PAGES_BASE_PATH = None
    SITE_MODULES_BASE_PATH = None
   
    SITE_PHOTO_LIMIT = -1
    SITE_NAME = None
    
    try:
    	user = request.user

    	
    
    except:
        pass
    
    
       
    try:
        SITE_PHOTO_LIMIT = settings.SITE_PHOTO_LIMIT
    except:
        pass
    
       
    try:
        SITE_NAME = settings.SITE_NAME
    except:
        pass
    
    try:
        MEDIA_PATH_SITE_REPOSITORY = settings.MEDIA_PATH_SITE_REPOSITORY
    except:
        pass
    
    
    
    try:
       MEDIA_URL_SITE_REPOSITORY = settings.MEDIA_URL_SITE_REPOSITORY
    except:
        pass

    try:

       SITE_TITLE = settings.SITE_TITLE

    except:
        pass

    try:

       SITE_TEMPLATE_PAGES_BASE_PATH = settings.SITE_TEMPLATE_PAGES_BASE_PATH

    except:
        pass

    try:
       SITE_MODULES_BASE_PATH = settings.SITE_MODULES_BASE_PATH
    except:
        pass

    return {
            'SITE' : curr_site.domain,
            'MOVIE_NO_PICS':MOVIE_NO_PICS,
            'MOVIE_NO_ORI':MOVIE_NO_ORI,
            'PREVIEW_URL' : PREVIEW_URL,
            'MEDIA_URL' : settings.MEDIA_URL,
            'MEDIA_PATH_SITE_REPOSITORY' : MEDIA_PATH_SITE_REPOSITORY,
            'MEDIA_URL_SITE_REPOSITORY' : MEDIA_URL_SITE_REPOSITORY,
            'SITE_TITLE' : SITE_TITLE,
            'SITE_TEMPLATE_PAGES_BASE_PATH' : SITE_TEMPLATE_PAGES_BASE_PATH,
            'SITE_MODULES_BASE_PATH' : SITE_MODULES_BASE_PATH,
            'SITE_PHOTO_LIMIT' : SITE_PHOTO_LIMIT,
            'SITE_NAME' : SITE_NAME,
           
            }


from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL
  
    path(route='', view=views.get_dealerships, name='index'),
    # path for about view
    path(route='about/', view=views.about, name='about-view'),
    # path for contact us view
    path(route='contact/', view=views.contact, name='contact-view'),
    # path for logout
    path(route='logout/', view=views.logout_request, name='logout-view'),
    # path for login
    path(route='login/', view=views.login_request, name='login-view'),
    # path for registration
    path(route='registration/', view=views.registration_request, name='registration-view'),
    # path for dealer details/reviews
    path(route='dealer/<int:dealer_id>/', view=views.get_dealer_details, name='dealer-details-view'),
    # path for add a review view
    path(route='review/<int:dealer_id>/', view=views.add_review, name='add-review-view'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
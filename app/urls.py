"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from public import views as publicviews
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
#user routings
userurlpatterns = ([
    path('', publicviews.signup_user, name="register"),
    path('get-by-email/<email>',publicviews.get_user_by_email_address)
])

venueurlpatterns = ([
    path('', publicviews.venues, name="venue"),
    path('add-student/', publicviews.add_venue, name="add_student"),
    path('save-student/', publicviews.save_student),
    path('<venue_id>', publicviews.edit_venue, name="edit_venue"),
    path('update-venue/', publicviews.update_venue, name="update_venue"),
    path('delete-venue/',publicviews.delete_venue,name="delete_venue")
])

bookingurlpatterns = ([
    path('approve-booking/', publicviews.approve_booking, name="approve_booking"),
    path('delete-booking/',publicviews.delete_booking,name="delete_booking")
])
    
collectorurlpatterns = ([
    path('', publicviews.collectors, name="collectors"),
    path('add-collector/', publicviews.add_collector, name="add_collector"),
    path('save-collector/', publicviews.save_collector),
    path('<venue_id>', publicviews.edit_venue, name="edit_venue"),
    path('update-venue/', publicviews.update_venue, name="update_venue"),
    path('delete-venue/',publicviews.delete_venue,name="delete_venue")
])   

collectordashboardurlpatterns = ([
        path('',publicviews.collector_dashboard,name = "collector_dashboard"),
         path('pickup/<int:id>',publicviews.pickup,name = "pickup"),
         path('deliver/<int:id>',publicviews.deliver,name = "deliver"),
         path('giverepair/<int:id>',publicviews.giverepair,name = "giverepair"),
         path('collectrepair/<int:id>',publicviews.collectrepair,name = "collectrepair"),
          path('updatestatus/<int:id>',publicviews.updatestatus,name = "updatestatus"),
                  
        ])  
    
    
dashboardurlpatterns = ([
    path('', publicviews.dashboard, name="dashboard"),
    path('students/', include(venueurlpatterns)),
    path('collectors/', include(collectorurlpatterns)),
    path('assign-phone/<int:pk>',publicviews.assignphone,name = 'assign-phone'),
    path('save_assign/<int:id>',publicviews.save_assign,name = "save_assign"),
    path('bookings/',include(bookingurlpatterns))
])


authurlpatterns = ([
    path('', publicviews.user_login, name="user_login"),
    path('edit-profile/', publicviews.edit_profile, name="edit_profile"),
    path('update-user/', publicviews.update_user, name="update_user"),
    path('logout/',publicviews.logout,name="logout")
])


publicurlpatterns = ([
    path('', publicviews.home, name='home'), #in use
    path('termsandconditions/',publicviews.termsandconditions, name = 'termsandconditions'),
    path('login/', publicviews.login, name="login"), # in use
    path('signup/', publicviews.signup, name="signup"), # in use
    path('dashboard/', include(dashboardurlpatterns)),
    path('collector_dashboard/',include(collectordashboardurlpatterns)),
    path('users/', include(userurlpatterns)),
    path('auth/', include(authurlpatterns)), # in use
    path('venue/<venue_id>', publicviews.view_venue, name="venue"),
    path('venue/in/<category>', publicviews.get_venues_by_category, name="get_venues_by_category"),
    path('book/<venue_id>', publicviews.book_venue, name="book_venue"),
    path('gift-phone/', publicviews.GiftPhone.as_view(), name="gift-phone"), #in use # old name = put_order
    path('success/',publicviews.success,name = "success"), #in use
    #publicviews.booking_success, name="booking_success"),
    path('venues/', publicviews.all_venues, name="all_venues"),
    path('venues/at/<location>', publicviews.venues_by_location, name="venues_by_location"),
    path('venues/by/<sort_by>',publicviews.venues_sort_by,name="venues_sort_by")
])


urlpatterns = [
    path('', include(publicurlpatterns)),
    path('admin/', admin.site.urls),
    #path('admin/', include(adminurlpatterns))
]

handler404 = 'public.views.not_found_error'

urlpatterns = urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

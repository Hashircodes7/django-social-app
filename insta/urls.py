from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from . import views
from .views import (
    createpostview,
    updatepostview,
    confirmdeletepostview,
    postdetailview,
    createcomment,
    togglecommentlike,
    togglepostlike,
    togglefollowview
    )

urlpatterns = [
    path('index/',views.homeview,name='index'),
    path('explore/',views.exploreview,name='explore'),
    path('register/',views.useregisterview,name='register'),
    path('login/',views.userloginview,name='login'),
    path('logout/',views.userlogoutview,name='logout'),
    path('post/create/',createpostview.as_view(),name='createpost'),
    path('post/<int:pk>/update/',updatepostview.as_view(),name='updatepost'),
    path('post/<int:pk>/delete/',confirmdeletepostview.as_view(),name='deletepost'),
    path('user/<int:user_id>/follow',togglefollowview.as_view(),name='togglefollow'),
    path('post/<int:postid>/comment/',createcomment.as_view(),name='createcomment'),
    path('post/<int:postid>/like/',togglepostlike.as_view(),name='likepost'),
    path('post/<int:pk>/', postdetailview.as_view(), name='postdetail'),
    path('comment/<int:commentid>/like/', togglecommentlike.as_view(),name='likecomment')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
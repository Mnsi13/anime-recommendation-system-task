
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import RegisterView, UserPreferencesView, AnimeSearchView, AnimeRecommendationView,WatchedAnimeView

urlpatterns = [
    path('auth/register/', RegisterView.as_view()),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # from rest_framework_simplejwt.views
    path('user/preferences/', UserPreferencesView.as_view()),
    path('anime/search/', AnimeSearchView.as_view()),
    path('anime/recommendations/', AnimeRecommendationView.as_view()),
    
    #I have added the extra functionality where we can see 
    # anime watched by user and also dlt by id
    path('anime/watched/', WatchedAnimeView.as_view()),
    path('anime/watched/<int:pk>/', WatchedAnimeView.as_view()),
]
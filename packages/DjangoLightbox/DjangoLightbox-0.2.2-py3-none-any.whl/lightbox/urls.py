from django.urls import path
from lightbox.views import ImagePageView

app_name = 'lightbox'
urlpatterns = [
    path('<int:pk>/<str:path>/<int:page>', 
    ImagePageView.as_view(), name="lightbox-page"),
]
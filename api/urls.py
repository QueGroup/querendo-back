from django.urls import (
    path,
    include,
)

from api.spectacular.urls import (
    urlpatterns as doc_urls,
)
from swipes.urls import (
    urlpatterns as swipes_url,
)
from users.urls import (
    urlpatterns as user_urls,
)

app_name = 'API'

urlpatterns = [
    path('auth/', include('djoser.urls.jwt'))
]

urlpatterns += doc_urls
urlpatterns += user_urls
# urlpatterns += matches_urls
urlpatterns += swipes_url

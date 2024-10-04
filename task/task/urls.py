from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('adminpanel/', include('app.urls',namespace='adminpanel')),
    path('teacher/', include('Teacher.urls',namespace='teacher')),
    path('student/', include('Student.urls',namespace='student')),
]

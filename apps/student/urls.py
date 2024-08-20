from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet,StudentDetails,CreateStudent,UpdateStudentDetails,DeleteStudentDetails

router = DefaultRouter()
router.register(r'student', StudentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('student-details/<int:pk>/', StudentDetails.as_view({'get': 'list'}), name='student-detail'),
    path('student-create/', CreateStudent.as_view({'post': 'post'}), name='student-create'),
    path('student-update/<int:pk>/', UpdateStudentDetails.as_view({'put': 'update'}), name='student-update'),
    path('student-delete/', DeleteStudentDetails.as_view({'delete': 'delete'}), name='student-delete'),

]

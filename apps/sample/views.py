from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

from apps.sample.models import Question
from apps.sample.serializers import QuestionSerializer
from core.permissions import StrictDjangoModelPermissions
from core.viewsets import ModelViewSet


def index(request, *args, **kwargs):
    from django.contrib.auth.mixins import LoginRequiredMixin
    name = f" {request.user.email}" if request.user.is_authenticated else ''
    return HttpResponse(f"Welcome{name},<br> to index page.")


class QuestionsViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    search_fields = ('question',)

    ordering_fields_mapping = {
        'question_options': 'question'
    }
    ordering_fields = ('id')
    ordering = 'id'

    filterset_fields_mappings = {
        'question_contains': ('question', 'icontains'),
        'question_c': 'question',
    }
    filterset_fields = ['question']

    permission_classes = [IsAuthenticated, StrictDjangoModelPermissions]
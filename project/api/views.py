#from django.shortcuts import render
from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import SurveyModel, QuestionModel, AnswerModel, AnonymousUserModel
from .serializers import (
        SurveySerializer, SurveySerializerWithoutStartDate, QuestionSerializer,
        AnswerSerializer
    )
from .permission import AnonymousUserIsSetIdentifier
from .tools import get_anonymous_identify_model, build_survey_tree_by_answers

# Create your views here.

class SurveyViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = SurveySerializer
    serializer_class_no_change_start_date = SurveySerializerWithoutStartDate

    queryset = SurveyModel.objects.all()

    def get_serializer_class(self):
        ''' No change start date after create survey '''
        serializer_class = self.serializer_class

        if self.request.method == 'PUT':
            # Show update form without start date field
            serializer_class = self.serializer_class_no_change_start_date

        return serializer_class


class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = QuestionSerializer
    queryset = QuestionModel.objects.all()


class ActiveSurveysListView(views.APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        return Response(SurveyModel.get_list_names_active_surveys())


class AnswerToTheQuestionView(viewsets.ModelViewSet):
    permission_classes = (AnonymousUserIsSetIdentifier, )
    serializer_class = AnswerSerializer
    queryset = AnswerModel.objects.all()

    def get_queryset(self):
        query_set = self.queryset.filter(
                        anonymous_user=get_anonymous_identify_model(
                                            self.request))
        return query_set


class ShowSurveysUserView(views.APIView):
    permission_classes = (AnonymousUserIsSetIdentifier, )

    def get(self, request):
        user_identify = get_anonymous_identify_model(request)

        return Response(
                build_survey_tree_by_answers(
                    user_identify.related_anonymous_user.all()))

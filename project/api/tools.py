from django.http.request import HttpRequest
from django.db.models.query import EmptyQuerySet
from rest_framework.exceptions import PermissionDenied

from .models import AnonymousUserModel


def get_anonymous_identify_model_id(request: HttpRequest) -> str:
    return get_anonymous_identify_model(request).id


def get_anonymous_identify_model(request: HttpRequest) -> AnonymousUserModel:
    ''' The user ID instance is returned. If the user is not registered,
        the identifier must be specified in the path parameters.
    '''

    if request.user.is_authenticated:
        object, created = AnonymousUserModel.objects.get_or_create(
                                user=request.user)
        return object

    identifier = request.GET.get('identifier')

    if identifier:
        object, created = AnonymousUserModel.objects.get_or_create(
                                identifier=identifier)
    else:
        raise PermissionDenied(
                detail='Please add AnonymousUserID to URL parameters',
                code=410)

    return object


def build_survey_tree_by_answers(queryset: EmptyQuerySet) -> dict:
    ''' Build tree like this:

        survey:
            question:
                answer
            question:
                answer
    '''

    surveys = {}

    for answer in queryset:
        _dict_question = {
            'text': answer.question.text,
        }

        if answer.text:
            _dict_question['answer_text'] = answer.text

        list_choices_user = []
        for selected in answer.selected_choices.all():
            list_choices_user.append(selected.choice_text)

        if list_choices_user:
            _dict_question['choices'] = list_choices_user

        survey = answer.question.survey

        try:
            _tmp = surveys['%d' % survey.id]['questions']
            _tmp.append(_dict_question)
        except KeyError:
            surveys['%d' % survey.id] = {
                    'name': survey.name,
                    'description': survey.description,
                    'info': survey.dates_info,
                    'questions': [_dict_question]
                }

    return surveys

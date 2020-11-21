import json

from django.conf import settings

from rest_framework import serializers

from .models import (
        SurveyModel, QuestionModel, ChoiceOptionModel, AnswerModel,
        AnonymousUserModel
    )
from .tools import get_anonymous_identify_model_id


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChoiceOptionModel
        fields = ('id', 'choice_text', )


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, required=False)

    class Meta:
        model = QuestionModel
        fields = ('id', 'text', 'choices', )

    def create(self, validated_data):
        choices = validated_data.pop('choices', None)

        question_instance = self.Meta.model.objects.create(**validated_data)

        if choices:
            choices_serializer = ChoiceSerializer(data=choices, many=True)
            if not choices_serializer.is_valid():
                return choices_serializer.errors

            choices_serializer.save(question_id=question_instance.id)

        return question_instance

    def update(self, instance, validated_data):
        choices = validated_data.pop('choices', None)
        choices_list = list(instance.choices)

        instance.text = validated_data.get('text', instance.text)
        instance.save()

        for choice_data in choices:
            choice = choices_list.pop(0)
            choice.choice_text = choice_data.get('choice_text',
                                                 choice.choice_text)
            choice.save()

        return instance


class SurveySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=False)

    datetime_start = serializers.DateTimeField(required=False)
    datetime_end = serializers.DateTimeField()

    class Meta:
        model = SurveyModel
        fields = ('id', 'name', 'description', 'datetime_start', 'datetime_end',
                  'questions', )

    def create(self, validated_data):
        questions = validated_data.pop('questions', None)

        survey_instance = self.Meta.model.objects.create(**validated_data)

        if questions:
            questions_serializer = QuestionSerializer(data=questions, many=True)
            if not questions_serializer.is_valid():
                return questions_serializer.errors

            questions_serializer.save(survey_id=survey_instance.id)

        return survey_instance


class SurveySerializerWithoutStartDate(serializers.ModelSerializer):
    datetime_end = serializers.DateTimeField(required=False)

    class Meta:
        model = SurveyModel
        fields = ('id', 'name', 'description', 'datetime_end')


class AnswerSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(
                    queryset=QuestionModel.objects.all())
    text = serializers.CharField(required=False)
    selected_choices = serializers.PrimaryKeyRelatedField(
                            many=True, queryset=ChoiceOptionModel.objects.all())

    class Meta:
        model = AnswerModel
        fields = ('id', 'question', 'text', 'selected_choices')

    def create(self, validated_data):
        selected_choices = validated_data.pop('selected_choices', None)

        validated_data['anonymous_user_id'] = get_anonymous_identify_model_id(
                                                    self.context['request'])
        created_answer = self.Meta.model.objects.create(**validated_data)

        created_answer.selected_choices.add(*selected_choices)
        created_answer.save()

        return created_answer

    def update(self, instance, validated_data):
        validated_data['anonymous_user_id'] = get_anonymous_identify_model_id(
                                                    self.context['request'])
        return super(AnswerSerializer, self).update(instance, validated_data)

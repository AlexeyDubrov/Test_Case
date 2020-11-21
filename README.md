## Установка и настройка

Создание и активация виртуальной среды. Установка всех необходимых пакетов.
```python
virtualenv .virtual
source .virtual/bin/activate
pip install -r requirements.txt
```

Запуск django
```python
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```


## API

### Аутентификация и дальнейшая авторизация.
```bash
post http://127.0.0.1:8000/auth/token/ '{username:test_username, password:test_password}'
```
В ответ на запрос, ожидается два токена. Для дальнейшей авторизации будет указыватся токен из `access`

```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MDU4OTkxOTgsImp0aSI6IjMyNmM5YzUxMTk2ZjQ4NGU4OTYwZTFhYmMxOTgwMDk0IiwidG9rZW5fdHlwZSI6ImFjY2VzcyIsInVzZXJfaWQiOjF9.t5b2kqUVprbizNQrowMD50b1s0bVk98qfwvlzDBEjag",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MDU5ODUyOTgsImp0aSI6ImFlZTdiMzY3NTc2NjQwMjE5NzZiMTE4NDA5OWUzNjJiIiwidG9rZW5fdHlwZSI6InJlZnJlc2giLCJ1c2VyX2lkIjoxfQ.PCySDorBpCswLmz6E2s_xcgWndbSIAZ1zbrDVrayckc"
}
```


### API администратора `/api/administrator/`.
Создание опроса с двумя вопросами и несколькими вариантами выбора.

```bash
# Send data to server with http header
post http://127.0.0.1:8000/api/administrator/surveys/ "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MDU4OTkxOTgsImp0aSI6IjMyNmM5YzUxMTk2ZjQ4NGU4OTYwZTFhYmMxOTgwMDk0IiwidG9rZW5fdHlwZSI6ImFjY2VzcyIsInVzZXJfaWQiOjF9.t5b2kqUVprbizNQrowMD50b1s0bVk98qfwvlzDBEjag"
```
```json
# POST data
{
    "name": "Опрос, какие фрукты любят пользователи.",
    "description": "Детальная информация по опросу",
    "datetime_start": "2020-11-19 19:42",
    "datetime_end": "2020-11-19 19:42",
    "questions": [{
        "text": "Первый вопрос. Какие фрукты больше нравятся?",
        "choices": [
            {
                "choice_text": "Яблоки"
            },
            {
                "choice_text": "Груши"
            },
            {
                "choice_text": "Персики"
            }
        ]
    },{
        "text": "Второй вопрос. Сколько готовы сьесть?",
        "choices": [
            {
                "choice_text": "Очень много"
            },
            {
                "choice_text": "Мало"
            }
        ]
    }]
}
```

### Ответ на вопрос.
Ответ на вопрос. Все данные сохраняются за идентификатором. Если пользователь вошел в систему, идентификатор указывать не нужно. Для наглядности, можно создать несколько ответов под разными идентификаторами и после чего просматривать ответы в зависимости от выбраного идентификатора `get http://127.0.0.1:8000/api/answers/?identifier=12345`

**selected_choices** - список **id** модели **ChoiceOptionModel**. Те варианты, которые выбрал пользователь.
```bash
# Send data to server
post http://127.0.0.1:8000/api/answers/?identifier=12345
```
```json
# POST data
{
    "question": 4,
    "text": "Какой-то расширенный ответ на вопрос!",
    "selected_choices": [
        3,
        5
    ]
}
```

### Информация по API.

```bash
# Get all surveys
get http://127.0.0.1:8000/api/administrator/surveys/ "Authorization: Bearer ..."

# Create new survey
post http://127.0.0.1:8000/api/administrator/surveys/ "Authorization: Bearer ..."

# Show detail survey
get http://127.0.0.1:8000/api/administrator/surveys/<id>/ "Authorization: Bearer ..."

# Delete survey
delete http://127.0.0.1:8000/api/administrator/surveys/<id>/ "Authorization: Bearer ..."
```

```bash
# Get all questions
get http://127.0.0.1:8000/api/administrator/questions/ "Authorization: Bearer ..."

# Update question
put http://127.0.0.1:8000/api/administrator/questions/<id>/ "Authorization: Bearer ..."

# Show detail question
get http://127.0.0.1:8000/api/administrator/questions/<id>/ "Authorization: Bearer ..."

# Delete question
delete http://127.0.0.1:8000/api/administrator/questions/<id>/ "Authorization: Bearer ..."
```

API для пользователей

```bash
# Get all surveys for users
get http://127.0.0.1:8000/api/list-active-surveys/
```

```bash
# Get all answers for users by identifier
get http://127.0.0.1:8000/api/answers/?identifier=12345
```

```bash
# Get all answered surveys by identifier
get http://127.0.0.1:8000/api/answered-surveys/?identifier=12345
```
```json
1: {
    "name": "Опрос, какие фрукты любят пользователи.",
    "description": "Детальная информация по опросу",
    "info": "Start survey 19 November 2020 (22:16). End 19 November 2020 (22:16)",
    "questions": [
        {
            "text": "Первый вопрос. Какаие из этих фруктов вам больше нравятся?",
            "choices": [
                "Яблоки",
                "Персики"
            ]
        }, {
            "text": "Второй вопрос. Почему они Вам нравятся?",
            "answer_text": "Потому что они вкусные!",
        }
    ]
}
```

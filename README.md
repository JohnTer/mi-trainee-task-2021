# Простой сервис для онлайн голосования

Краткая схема сервиса:
![Screenshot from 2021-06-17 10-59-02](https://user-images.githubusercontent.com/36763228/122356026-14086480-cf5b-11eb-8fd1-f42204dfc029.png)

Сервис реализует API работающее по протоколу HTTP. 

Реализованы методы:
* POST /api/createPoll/ создать голосование c вариантами ответов.
* POST /api/poll/ проголосовать за конкретный вариант.
* POST /api/getResult/ получить результат по конкретному голосованию.


### POST /api/createPoll/

Создает голосование с вариантами ответов. В теле передается JSON вида:
```json
{

    "name": "Какое авто лучше?",
    "answers": ["Audi", "BMW"]

}
```
Поле ```"name"``` является строкой и содержит название создаваемого опроса.
Поле ```"answers"``` является массивом строк и содержит варианты ответов создаваемого опроса.

В случае успешного создания задачи, в ответ возвращается код ответа *201* и JSON-объект c идентификатор опроса вида:

```json
{
    "poll_id": "d65056c6-71e6-42ef-acbc-dcb65dedc169"
}
```

В случае невалидного запроса, возвращается код *400*, и JSON, в поле ```"error"``` которого находится описание ошибки.

### POST /api/poll/
Данный метод позволяет проголосовать за определенный вариант опроса. В теле передается JSON вида:
```json
{
    "choice": "BMW",
    "poll_id": "d65056c6-71e6-42ef-acbc-dcb65dedc169"
}
```
Поле ```"poll_id"``` является строкой и содержит id существующего опроса.
Поле ```"choice"``` является строкой и содержит id один из вариантов опроса, за который отдается голос.

В случае успешного голосования, в ответ возвращается код ответа *200* и JSON-объект c идентификатор опроса.


В случае невалидного запроса, возвращается код *400*, и JSON, поле ```"error"``` которого находится описание ошибки. В случае несуществующего опроса или варианта ответа, возвращается возвращается код *404*, и JSON,  поле ```"error"``` которого находится подробное описание ошибки.

### POST /api/getResult/
Данный метод позволяет получить результат по конкретному голосованию. В теле передается JSON вида:

```json
{
    "poll_id": "d65056c6-71e6-42ef-acbc-dcb65dedc169"
}
```

Поле ```"poll_id"``` является строкой и содержит id существующего опроса.

В случае успешного голосования, в ответ возвращается код ответа *200* и JSON-объект c результатами опроса вида:
```json
{
    "name": "Какое авто лучше?",
    "answers": {
        "Audi": 0,
        "BMW": 1
    }
}
```

В случае невалидного запроса, возвращается код *400*, и JSON, поле ```"error"``` которого находится описание ошибки. В случае несуществующего опроса, возвращается возвращается код *404*, и JSON,  поле ```"error"``` которого находится подробное описание ошибки.

## Запуск сервиса

Для запуска сервиса, необходимо в корне проекта выполнить команду:  ```"docker-compose up"```

Сервис станет доступен на 8000 порту по умолчанию. Конфигурации доступны в папке *deploy*.

## Запуск тестов
Для тестирования сервиса, необходимо в корне проекта выполнить команду:  ```"pytest ./tests/"```

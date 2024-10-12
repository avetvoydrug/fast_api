# best_practices
- по заявлению создателей FastAPI:
    - asyncpg работает в 3 раза быстрее psycopg2
- советуют переименовывать миграции alembic, например в дату миграции + хэш, чтобы не путаться
- SQL Injections:
    - есть вероятность припрописании сырых запросов к БД
        - и подставлениие аргументов от пользователя в строку запроса
        - навредить БД
    - например:
        - пользователь передал user_id = '123; DROP TABLE users;
        - функция с запросом выглядит так:
        ```
        #Python
        def get_user_bio(user_id):
            query = f' SELECT * FROM users WHERE user_id = {user_id}'
            ...
        ```
        - Следовательно выполниться 2 запроса
            - 1) выберется вся инф-я о пользователе
            - 2) удалится таблица users
- построение эндпоинтов:
    - все эндпоинты должны выглядет примерно одинаково
    - обёрнут в try\except (отлов неожиданных ошибок)
        - при отлове неож. ошибок хорошей практикой будет куда-либо её занести:
        Напр: # "Передать ошибку разработчикам"
    - обрабатывает, конкретные ошибки (для удобства обратной связи пользователям)
    - одинаковая структура ответа для 200-х, 400-х и иных статусов (для удобства разработки)
# Записи
- роутер объединяет набор энд поинтов
- stmt: post, update, delete
- query: get
- постоянно забываю ORM: object-relation model (работа с таблцами, через объекты)
- "так получается с Алхимией, что нам нужно не просто сэкзэкьютить,
        а ещё забрать эти данные"
# REDIS
- БД, которая хранится в ОЗУ, формат key:value, написана на C молниеносная отдача данных
- кэширование пример
    - отдать сотне пользователей посчитанные данные за вчерашние события
- кэшируются уникальные связки func_name, args, kwargs
    - при добавлении аргументов или изменении чего0либо кэш пересчитывается
# Celery
## .delay()!!!
- для инициализации celery достаточно выбрать любое имя и обязательно указать адрес broker'a
- можно кастомизировать таски
- для запуска celery инициализируется новый процесс(ы) 
    - для запуска в несколько процессов windows не подходит
- при запуске делает 'слепок' кода и не изменяет его при внесённых
    изменениях во время выполнения, нет оф. решения 
- run cmd coomand:
    - <path> - относительно main.py
```
    celery -A <path.path>:celery worker --loglevel=INFO --pool=solo
```
- Варианты запуска:
    - 1) worker: принимает и тут же выполняет
    - 2) flower: http://localhost:5555/
    - 3) beat: периодические задания, e.g. send a report every day
## Flower
- Dashboard: список воркеров
- Tasks: список незавершённых задач
- Broker: адрес брокера(в нашем случае redis), где хранятся таски
# FastAPI funcs:
- startup/shutdown: настройки поведения при старте/остановке приложения
    -- мб не устарело, но сейчас в fastapi-cache подход иной
# Cookie, JWT, Redis, database
- куки хранятся у пользователя в браузере и передаются с каждым запросом
    - как понял - это транспорт, а уже дальше мы выбираем стратегию доставки
- JWT не можем убить токен, пока он сам не доживёт свой цикл, хранится в браузере юзера
    - состоит из трёх частей xxx.xxx.xxx:
        - при запросах проверяем валидность подписи.
        - 1) алгоритм и тип аут
        - 2) содержимое, пароли и подобную чувствит инфу обычно не передают
        - 3) подпись (расшифровать нельзя, кодируется и декод. на бэкэнде, с помощью секретного ключа)
- redis, database надо каждый раз дёргать базу данных
    - с первым это происходит быстрее, но всё равно нужно думать как..

# Изменения в написании моделей после децентрализации БД из одного файла
- следует явно создавать переменную metadata:
```
#Python
from sqlalchemy import Metadata, Table
metadata = Metadata()

some_table = Table(
    'some_table',
    metadata,
    # Column('1')
    # Column('n')
)
```
## in database.py:
```metadata = Metadata()```
## в остальных:
```from database import metadata```
# Изменения в migrations/env.py после добавления второго и последующих приложений
- target_metadata = [metadata_1, metadata_2, metadata_n]
- metadata следует импортировать из каждого файла models.py

# alembic.ini changes:
- до:
- sqlalchemy.url = postgresql://%(DB_USER)s:%(DB_PASS)s@%(DB_HOST)s:%(DB_PORT)s/%(DB_NAME)s
- после:
- sqlalchemy.url = postgresql+asyncpg://%(DB_USER)s:%(DB_PASS)s@%(DB_HOST)s:%(DB_PORT)s/%(DB_NAME)s?async_fallback=True

# Pytest-asyncio
- 3 шага:
    1) выбор sync/async тестирования
    2) создание тестовой БД
    3) переписывание зависимостей
- тесты могут быть как внутри, так и вне папки приложения
- conftest.py: основной файл - входная точка
    создаются важные фикстуры, соединения с бд и т.д.
    - привязываем метаданные к движку, чтобы таблицы создавались именно в тестовой БД 
```
metadata.bind = engine_test
```

### pet:
- странички со статусами доступные только аут пользователям
- для не аутентифицированных
- для аут., но аут могут быть фэйки
- кастомные группы по приглашениям

### DockerFile
- Позволяет собирать приложение в контейнер
- #язык и версия
```FROM <lang>:<ver>```

-  #создание директории
```RUN mkdir /<create_dir_for_app>```

- #выбор рабочей дир
```WORKDIR /<create_dir_for_app```

- ниже | # первым делом устанавливаем зависимости, чтобы докер их кэшировал
    и не устанавливал каждый раз
- #Копирование файла с зависимостями в <.> - рабочая дир
    #requirements.txt делаем перед копированием остального кода, т.к. редко меняется
```COPY requirements.txt .```

- #установка зависимостей
```RUN pip install -r requirements.txt```

- #из папки с DokerFile <.> скопировать всё в <.> рабочую дир <create_dir_for_app>
```COPY . .```

- #для запуска bash-скриптов пользователю требуется разрешение
```RUN chmod a+x docker/*.sh```

- #т.к. запускаем приложение из src иначе будут не правильно работать импорты?
```WORKDIR src```

- #CMD запускается после сбора и запуска контейнера
    4 воркера по работе с запросами юзеров и указывается класс воркера обяз
- лучше быть "эксплисид" и указывать порт указывать порт, по дэфолту вроде 80 
```CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000```

- #Запуск DockerFile'a (сборка образа)
    <.> - текушая дир; <-t> -тэг имя:версия
```docker build . -t fastapi_app:latest```

- #Запуск
- Нужно прокинуть порты -p <any_port>:<port_from_cmd>
    <any_port> - порт, на котором мы хотим увидеть его на локальной машине
- -d детэч мод?
```docker run -d -p 7329:8000 fastapi_app```
```docker logs <from_console>```

### docker-compose.yml
- позволяет собирать несколько приложений в контейнер
```
#docker-compose.yml
version: '3.x'
services:
  db:
    image: postgres:17 # <image>:<ver>
    container_name: db_app # дать название контейнеру, если много подобных
    command: -p 1221 # задать кастомный порт, если уже занят дефолтный
    expose:
      - 1221 # относ. к command
    env_file:
      - <.envFileName> # название .env файла
  redis:
    image: redis:7
    container_name: redis_app
    command: -p 5370
    expose:
      - 5370
    env_file:
      - <.envFileName>
  app: # настройка для приложения
    build: # у нас нет image - у нас есть build
      context: . # <path> где находится DockerFile
    env_file:
      - <.envFileName>
    container_name: <name_app>
    command: ["/<dir>/docker/app.sh"] # в этом приложении сначала нужно прогнать миграции alembic
                                        # затем уже запускать gunicorn, поэтому так
                                        # из DockerFile'a убраны WORKDIR и CMD 
    ports:
      <localPort>:<enginePort> # 1 - порт на локал. машине; 2 - порт из DockerFile'a, на котором
                                # запускается движок
    depends_on: # устанавливаем зависимости, что за чем создавать
      - db
      - redis
  celery:
    build: # используем тоже самое, что и app, т.к. celery - это либа
      context: .
    env_file:
      - <.envFileName>
    command: ["<workdir>/<bash_script_dir>/fileName.sh", "arg"]
    container_name: celery_app
    depends_on:
      - redis # зависит от брокера из редис
  flower:
    build: 
      context: .
    env_file:
      - <.envFileName>
    command: ["<workdir>/<bash_script_dir>/fileName.sh", "flower"]
    container_name: flower_app
    depends_on:
      - redis
      - celery
```

### .env-non-dev
-   DB_HOST=db # обяз в докере
    DB_PORT=1221 # любой
    DB_NAME=postgres
    DB_USER=postgres
    DB_PASS=1234

    POSTGRES_DB=postgres # обяз в докере
    POSTGRES_USER=postgres # обяз в докере
    POSTGRES_PASSWORD=postgres # обяз в докере

    REDIS_HOST=redis # обяз в докере
    REDIS_PORT=5370 # любой
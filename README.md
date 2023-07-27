# Описание проекта QRKot:

Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

Ключевые возможности:
- создавать целевые проекты;
- собирать пожертвования от пользователей и распределять их по проектам.

### Используемые технологии:

Python 3.7, FastAPI 0.78.0

### Как запустить проект:

```
git clone https://github.com/olegtsss/cat_charity_fund.git
cd cat_charity_fund
python -m venv venv
. venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app
```

### Проекты:
В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.
Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект. 


### Пожертвования:
Каждый пользователь может сделать пожертвование и сопроводить его комментарием. Пожертвования не целевые: они вносятся в фонд, а не в конкретный проект. Каждое полученное пожертвование автоматически добавляется в первый открытый проект, который ещё не набрал нужную сумму. Если пожертвование больше нужной суммы или же в Фонде нет открытых проектов — оставшиеся деньги ждут открытия следующего проекта. При создании нового проекта все неинвестированные пожертвования автоматически вкладываются в новый проект.


### Пользователи:
Целевые проекты создаются администраторами сайта. 
Любой пользователь может видеть список всех проектов, включая требуемые и уже внесенные суммы. Это касается всех проектов — и открытых, и закрытых.
Зарегистрированные пользователи могут отправлять пожертвования и просматривать список своих пожертвований.


### API:
настроены эндпоинты:

```
/charity_project/ (GET, POST): получение имеющихся проектов и создание нового;
/charity_project/{id}/ (PATCH, DELETE): редактирование и удаление проекта;
/donation/ (GET, POST): получение имеющихся пожертвований или создание нового;
/donation/my/ (GET): получеие пожертвований, сделанных пользователем;
/auth/jwt/login (POST): получение токена пользователем;
/auth/jwt/logout (POST): деаунтификация пользователя;
/auth/register (POST): регистрация пользователя;
/users/me (GET, PATCH): получение информации о пользователе;
/users/{id} (PATCH): редактирование информации о пользователе;
/google/ (POST): получение информации о закрытых проектах в Google API;
```

## Документация:
[http://127.0.0.1:8000/docs]
[http://127.0.0.1:8000/redoc]



## Шаблон наполнения env-файла:

```
APP_TITLE=QRKot
DESCRIPTION=Благотворительный фонд поддержки котиков
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=123
FIRST_SUPERUSER_EMAIL=admin@admin.ru
FIRST_SUPERUSER_PASSWORD=123

```

### Разработчик:
[Тимощук Олег](https://github.com/olegtsss)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=whte)

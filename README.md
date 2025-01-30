# pyemias

**pyemias** — это неофициальная Python библиотека для автоматизированной записи через портал [EMIAS.INFO](https://emias.info) на прием к врачу.

## Описание

pyemias позволяет взаимодействовать с порталом EMIAS, используя Python, для автоматической записи на прием к врачу.

## Установка

```bash
pip install pyemias
```

Для установки последней версии из исходников:
```bash
git clone https://github.com/GvozdevAD/pyemias.git
cd pyemias
pip install .
```

## Пример использования

Простой пример использования библиотеки:

```python
from pprint import pprint
from pyemias import (
    EmiasClient, 
    AuthPolicyData
)


# Данные для авторизации
policy_data = {
    "policy_number": "0000000000000000", # Номер полиса из 16 символов
    "birth_date": "1900-01-01"           # Дата рождения в формате YYYY-MM-DD
}
auth_policy_data = AuthPolicyData(**policy_data)

# Создание экземпляра клиента
client = EmiasClient(auth_policy_data)
# Инициализация сессии
client.initialize()

# Если вы запускаете первый раз, сохраните jwt токен (действует 7 дней)
with open("jwt_token", "w", encoding="utf-8") as file:
    file.write(client.jwt_token)

# Получение информации о специализациях
specialities_info = client.get_specialities_info()
pprint(specialities_info)

# Получение информации о врачах по ID специальности
doctors_info = client.get_doctors_info(200)
pprint(doctors_info)

```
#### Использование контекстного менеджера

Библиотека поддерживает работу через контекстный менеджер для автоматического управления сессией:

```python
from pprint import pprint
from pyemias import (
    EmiasClient,
    AuthPolicyData
)


# Данные для авторизации
policy_data = {
    "policy_number": "0000000000000000", # Номер полиса из 16 символов
    "birth_date": "1900-01-01",          # Дата рождения в формате YYYY-MM-DD
    "jwt": "cdkew.cmkdas.caskdc"         # (Необязательно) Сохранённый JWT токен
}
auth_policy_data = AuthPolicyData(**policy_data)

with EmiasClient(auth_policy_data) as client:
    # Получение информации о специализациях
    specialities_info = client.get_specialities_info()
    pprint(specialities_info)
    
    # Получение информации о врачах по ID специальности
    doctors_info = client.get_doctors_info(200)
    pprint(doctors_info)
    
```
#### Примечания:
* Контекстный менеджер автоматически завершает сессию по окончании работы. Это особенно полезно для обработки исключений или при большом количестве запросов.
* Функция initialize требуется только при ручной инициализации клиента.
* JWT-токен необходимо сохранять, если вы планируете повторно использовать клиент в течение 7 дней без повторной авторизации.

## Методы

### `EmiasClient.get_specialities_info(as_dict: bool = False) -> (list[SpecialitiesResponse] | list[dict])`
Возвращает список специализаций, доступных для записи через портал EMIAS.

* Параметры:
    * as_dict (bool): Определяет формат возвращаемых данных.
        * Если True, возвращает список словарей (list[dict]).
        * Если False, возвращает список объектов SpecialitiesResponse.

* Возвращаемый тип:
    * list[SpecialitiesResponse] — по умолчанию.
    * list[dict] — если указан параметр as_dict=True.

### `EmiasClient.get_doctors_info(speciality_id: int)`
Возвращает информацию о врачах для указанной специальности.
* Параметры:
    * speciality_id (int): Идентификатор специальности.
* Возвращаемый тип: `list[dict]`


## Поддержка

Если у вас возникли вопросы или проблемы с использованием библиотеки, вы можете открыть [issue](https://github.com/GvozdevAD/pyemias/issues) на GitHub.

## Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для подробностей.
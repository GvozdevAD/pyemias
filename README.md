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
from datetime import datetime
from pyemias import EmiasClient
from pprint import pprint

# Создание экземпляра клиента
client = EmiasClient(
    policy_number="0000000000000000", 
    birth_date=datetime(1900, 1, 1),
    jwt_token="your_jwt_token"  # Опционально
)
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
from datetime import datetime
from pprint import pprint
from pyemias import EmiasClient


policy_number = "0000000000000000"
birth_date = datetime(1900, 1, 1)
with open("jwt_token", "r", encoding="utf-8") as file:
    jwt = file.read()

with EmiasClient(policy_number, birth_date, jwt) as client:
    # Получение информации о специализациях
    specialities_info = client.get_specialities_info()
    pprint(specialities_info)
    
    # Получение информации о врачах по ID специальности
    doctors_info = client.get_doctors_info(200)
    pprint(doctors_info)
    
```


## Методы

### `EmiasClient.get_specialities_info()`
Возвращает список специализаций, доступных для записи через портал EMIAS.
* Возвращаемый тип: `list[dict]`

### `EmiasClient.get_doctors_info(speciality_id: int)`
Возвращает информацию о врачах для указанной специальности.
* Параметры:
    * speciality_id (int): Идентификатор специальности.
* Возвращаемый тип: `list[dict]`


## Поддержка

Если у вас возникли вопросы или проблемы с использованием библиотеки, вы можете открыть [issue](https://github.com/GvozdevAD/pyemias/issues) на GitHub.

## Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для подробностей.
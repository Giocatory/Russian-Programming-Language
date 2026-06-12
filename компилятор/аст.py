# -*- coding: utf-8 -*-
"""
Узлы абстрактного синтаксического дерева (АСД) языка Сибиряк
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any, Union


# ─── Базовый узел ───────────────────────────────────────────────────────────

@dataclass
class УзелАСД:
    строка: int = 0
    столбец: int = 0


# ─── Типы ────────────────────────────────────────────────────────────────────

@dataclass
class ПростойТип(УзелАСД):
    имя: str = ''


@dataclass
class СрезТип(УзелАСД):
    элемент: 'ЛюбойТип' = None


@dataclass
class МассивТип(УзелАСД):
    размер: 'ЛюбойВыражение' = None
    элемент: 'ЛюбойТип' = None


@dataclass
class КартаТип(УзелАСД):
    ключ: 'ЛюбойТип' = None
    значение: 'ЛюбойТип' = None


@dataclass
class УказательТип(УзелАСД):
    база: 'ЛюбойТип' = None


@dataclass
class КаналТип(УзелАСД):
    элемент: 'ЛюбойТип' = None
    направление: str = 'оба'  # 'оба', 'отправить', 'получить'


@dataclass
class ФункцияТип(УзелАСД):
    параметры: List['ПолеПараметра'] = field(default_factory=list)
    результаты: List['ЛюбойТип'] = field(default_factory=list)


@dataclass
class ИнтерфейсТип(УзелАСД):
    методы: List['МетодИнтерфейса'] = field(default_factory=list)


@dataclass
class СтруктТип(УзелАСД):
    поля: List['ПолеСтруктуры'] = field(default_factory=list)


ЛюбойТип = Union[
    ПростойТип, СрезТип, МассивТип, КартаТип, УказательТип,
    КаналТип, ФункцияТип, ИнтерфейсТип, СтруктТип
]


# ─── Объявления ──────────────────────────────────────────────────────────────

@dataclass
class ПолеСтруктуры(УзелАСД):
    имена: List[str] = field(default_factory=list)
    тип: ЛюбойТип = None
    тег: Optional[str] = None


@dataclass
class МетодИнтерфейса(УзелАСД):
    имя: str = ''
    тип: ФункцияТип = None


@dataclass
class ПолеПараметра(УзелАСД):
    имена: List[str] = field(default_factory=list)
    тип: ЛюбойТип = None
    вариадик: bool = False


@dataclass
class ОбъявлениеФункции(УзелАСД):
    имя: str = ''
    получатель: Optional['ПолеПараметра'] = None
    параметры: List[ПолеПараметра] = field(default_factory=list)
    результаты: List[ЛюбойТип] = field(default_factory=list)
    тело: Optional['БлокОператоров'] = None
    экспортируется: bool = False


@dataclass
class ОбъявлениеСтруктуры(УзелАСД):
    имя: str = ''
    тип: СтруктТип = None
    экспортируется: bool = False


@dataclass
class ОбъявлениеИнтерфейса(УзелАСД):
    имя: str = ''
    тип: ИнтерфейсТип = None
    экспортируется: bool = False


@dataclass
class ОбъявлениеПеременной(УзелАСД):
    имена: List[str] = field(default_factory=list)
    тип: Optional[ЛюбойТип] = None
    значения: List['ЛюбойВыражение'] = field(default_factory=list)


@dataclass
class ОбъявлениеКонстанты(УзелАСД):
    имена: List[str] = field(default_factory=list)
    тип: Optional[ЛюбойТип] = None
    значения: List['ЛюбойВыражение'] = field(default_factory=list)


@dataclass
class ОбъявлениеТипа(УзелАСД):
    имя: str = ''
    тип: ЛюбойТип = None


@dataclass
class ИмпортСпецификация(УзелАСД):
    псевдоним: Optional[str] = None
    путь: str = ''


# ─── Операторы ───────────────────────────────────────────────────────────────

@dataclass
class БлокОператоров(УзелАСД):
    операторы: List['ЛюбойОператор'] = field(default_factory=list)


@dataclass
class ОператорВозврата(УзелАСД):
    значения: List['ЛюбойВыражение'] = field(default_factory=list)


@dataclass
class ОператорЕсли(УзелАСД):
    инициализация: Optional['ЛюбойОператор'] = None
    условие: 'ЛюбойВыражение' = None
    тогда: БлокОператоров = None
    иначе: Optional[Union[БлокОператоров, 'ОператорЕсли']] = None


@dataclass
class ОператорДля(УзелАСД):
    инициализация: Optional['ЛюбойОператор'] = None
    условие: Optional['ЛюбойВыражение'] = None
    пост: Optional['ЛюбойОператор'] = None
    тело: БлокОператоров = None
    # Для диапазон
    ключ: Optional[str] = None
    значение: Optional[str] = None
    итерируемое: Optional['ЛюбойВыражение'] = None
    тип_цикла: str = 'обычный'  # 'обычный', 'бесконечный', 'диапазон'


@dataclass
class ОператорПереключить(УзелАСД):
    инициализация: Optional['ЛюбойОператор'] = None
    выражение: Optional['ЛюбойВыражение'] = None
    случаи: List['СлучайПереключителя'] = field(default_factory=list)


@dataclass
class СлучайПереключателя(УзелАСД):
    выражения: List['ЛюбойВыражение'] = field(default_factory=list)  # пусто = умолчание
    тело: List['ЛюбойОператор'] = field(default_factory=list)


@dataclass
class ОператорКороткогоОбъявления(УзелАСД):
    имена: List[str] = field(default_factory=list)
    значения: List['ЛюбойВыражение'] = field(default_factory=list)


@dataclass
class ОператорПрисваивания(УзелАСД):
    цели: List['ЛюбойВыражение'] = field(default_factory=list)
    оператор: str = '='
    значения: List['ЛюбойВыражение'] = field(default_factory=list)


@dataclass
class ОператорВыражения(УзелАСД):
    выражение: 'ЛюбойВыражение' = None


@dataclass
class ОператорИнкремента(УзелАСД):
    выражение: 'ЛюбойВыражение' = None
    оператор: str = '++'


@dataclass
class ОператорПрервать(УзелАСД):
    метка: Optional[str] = None


@dataclass
class ОператорПродолжить(УзелАСД):
    метка: Optional[str] = None


@dataclass
class ОператорПерейти(УзелАСД):
    метка: str = ''


@dataclass
class ОператорМетки(УзелАСД):
    имя: str = ''
    оператор: 'ЛюбойОператор' = None


@dataclass
class ОператорОтложить(УзелАСД):
    вызов: 'ВызовФункции' = None


@dataclass
class ОператорГорутины(УзелАСД):
    вызов: 'ВызовФункции' = None


@dataclass
class ОператорВыбора(УзелАСД):
    случаи: List['СлучайВыбора'] = field(default_factory=list)


@dataclass
class СлучайВыбора(УзелАСД):
    оператор: Optional['ЛюбойОператор'] = None  # None = умолчание
    тело: List['ЛюбойОператор'] = field(default_factory=list)


ЛюбойОператор = Union[
    БлокОператоров, ОператорВозврата, ОператорЕсли, ОператорДля,
    ОператорПереключить, ОператорКороткогоОбъявления, ОператорПрисваивания,
    ОператорВыражения, ОператорИнкремента, ОбъявлениеПеременной,
    ОбъявлениеКонстанты, ОператорПрервать, ОператорПродолжить,
    ОператорПерейти, ОператорМетки, ОператорОтложить, ОператорГорутины
]


# ─── Выражения ───────────────────────────────────────────────────────────────

@dataclass
class ЛитералЦелого(УзелАСД):
    значение: int = 0
    исходник: str = ''


@dataclass
class ЛитералВещественного(УзелАСД):
    значение: float = 0.0
    исходник: str = ''


@dataclass
class ЛитералСтроки(УзелАСД):
    значение: str = ''


@dataclass
class ЛитералРуны(УзелАСД):
    значение: str = ''


@dataclass
class ЛитералИстина(УзелАСД):
    pass


@dataclass
class ЛитералЛожь(УзелАСД):
    pass


@dataclass
class ЛитералНоль(УзелАСД):
    pass


@dataclass
class Идентификатор(УзелАСД):
    имя: str = ''


@dataclass
class БинарноеВыражение(УзелАСД):
    левое: 'ЛюбойВыражение' = None
    оператор: str = ''
    правое: 'ЛюбойВыражение' = None


@dataclass
class УнарноеВыражение(УзелАСД):
    оператор: str = ''
    операнд: 'ЛюбойВыражение' = None


@dataclass
class ВызовФункции(УзелАСД):
    функция: 'ЛюбойВыражение' = None
    аргументы: List['ЛюбойВыражение'] = field(default_factory=list)
    вариадик: bool = False


@dataclass
class ДоступКПолю(УзелАСД):
    объект: 'ЛюбойВыражение' = None
    поле: str = ''


@dataclass
class Индексирование(УзелАСД):
    объект: 'ЛюбойВыражение' = None
    индекс: 'ЛюбойВыражение' = None


@dataclass
class Срезание(УзелАСД):
    объект: 'ЛюбойВыражение' = None
    низ: Optional['ЛюбойВыражение'] = None
    верх: Optional['ЛюбойВыражение'] = None
    макс: Optional['ЛюбойВыражение'] = None


@dataclass
class ЛитералСтруктуры(УзелАСД):
    тип: ЛюбойТип = None
    поля: List['ПолеЛитерала'] = field(default_factory=list)


@dataclass
class ПолеЛитерала(УзелАСД):
    ключ: Optional[str] = None
    значение: 'ЛюбойВыражение' = None


@dataclass
class ЛитералСреза(УзелАСД):
    тип: ЛюбойТип = None
    элементы: List['ЛюбойВыражение'] = field(default_factory=list)


@dataclass
class ЛитералКарты(УзелАСД):
    тип: КартаТип = None
    пары: List[tuple] = field(default_factory=list)  # (ключ, значение)


@dataclass
class ПреобразованиеТипа(УзелАСД):
    тип: ЛюбойТип = None
    выражение: 'ЛюбойВыражение' = None


@dataclass
class ВыражениеКанала(УзелАСД):
    канал: 'ЛюбойВыражение' = None


@dataclass
class АнонимнаяФункция(УзелАСД):
    параметры: List[ПолеПараметра] = field(default_factory=list)
    результаты: List[ЛюбойТип] = field(default_factory=list)
    тело: БлокОператоров = None


ЛюбойВыражение = Union[
    ЛитералЦелого, ЛитералВещественного, ЛитералСтроки, ЛитералРуны,
    ЛитералИстина, ЛитералЛожь, ЛитералНоль, Идентификатор,
    БинарноеВыражение, УнарноеВыражение, ВызовФункции, ДоступКПолю,
    Индексирование, Срезание, ЛитералСтруктуры, ЛитералСреза, ЛитералКарты,
    ПреобразованиеТипа, ВыражениеКанала, АнонимнаяФункция
]


# ─── Файл программы ──────────────────────────────────────────────────────────

@dataclass
class ФайлПрограммы(УзелАСД):
    пакет: str = ''
    импорты: List['ИмпортСпецификации'] = field(default_factory=list)
    объявления: List[Any] = field(default_factory=list)


@dataclass
class ИмпортСпецификации(УзелАСД):
    спецификации: List[ИмпортСпецификация] = field(default_factory=list)

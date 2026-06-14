#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'компилятор'))

from лексер import Лексер, ОшибкаЛексера
from парсер import Парсер, ОшибкаПарсера
from генератор_rust import ГенераторRust

# Тест 1: Простая программа
code = '''
пакет главный
функ Главная() { }
'''
л = Лексер(code)
т = л.токенизировать()
п = Парсер(т)
а = п.разобрать_файл()
г = ГенераторRust()
rust = г.генерировать(а)
with open('test1.rs', 'w', encoding='utf-8') as f:
    f.write(rust)
print('test1.rs created')

# Тест 2: Программа с функцией
code = '''
пакет главный
функ квадрат(х цел) цел { возврат х * х }
функ Главная() { квадрат(5) }
'''
л = Лексер(code)
т = л.токенизировать()
п = Парсер(т)
а = п.разобрать_файл()
г = ГенераторRust()
rust = г.генерировать(а)
with open('test2.rs', 'w', encoding='utf-8') as f:
    f.write(rust)
print('test2.rs created')

# Тест 3: Программа с печатью
code = '''
пакет главный
импорт "фмт"
функ Главная() { фмт.ПечатьФ("Привет, мир!\\n") }
'''
л = Лексер(code)
т = л.токенизировать()
п = Парсер(т)
а = п.разобрать_файл()
г = ГенераторRust()
rust = г.генерировать(а)
with open('test3.rs', 'w', encoding='utf-8') as f:
    f.write(rust)
print('test3.rs created')

# Тест 4: Программа с переменными
code = '''
пакет главный
функ Главная() { х := 42; }
'''
л = Лексер(code)
т = л.токенизировать()
п = Парсер(т)
а = п.разобрать_файл()
г = ГенераторRust()
rust = г.генерировать(а)
with open('test4.rs', 'w', encoding='utf-8') as f:
    f.write(rust)
print('test4.rs created')

print('All tests completed')

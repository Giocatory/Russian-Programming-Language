#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Компилятор языка Сибиряк — главная точка входа
Конвейер: .сбк → Лексер → АСД → Генератор Rust → rustc → исполняемый файл
"""

import sys, os, subprocess, tempfile, argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from лексер import Лексер, ОшибкаЛексера
from парсер import Парсер, ОшибкаПарсера
from генератор_rust import ГенераторRust, ОшибкаГенератора

ВЕРСИЯ = '0.2.0'

БАННЕР = r"""
  ╔═══════════════════════════════════════════════════╗
  ║        С И Б И Р Я К  —  компилятор v{ver}        ║
  ║     Русскоязычный язык программирования           ║
  ║     Бэкенд: Rust  •  Расширение: .сбк             ║
  ╚═══════════════════════════════════════════════════╝
""".format(ver=ВЕРСИЯ)


def токенизировать(исходник, имя_файла):
    try:
        return Лексер(исходник).токенизировать()
    except ОшибкаЛексера as e:
        print(f'\033[31m[Лексер] {e}\033[0m', file=sys.stderr); sys.exit(1)

def разобрать(токены, имя_файла):
    try:
        return Парсер(токены).разобрать_файл()
    except ОшибкаПарсера as e:
        print(f'\033[31m[Парсер] {e}\033[0m', file=sys.stderr); sys.exit(1)

def сгенерировать_rust(аст, имя_файла):
    try:
        return ГенераторRust().генерировать(аст)
    except ОшибкаГенератора as e:
        print(f'\033[31m[Генератор] {e}\033[0m', file=sys.stderr); sys.exit(1)

def скомпилировать_rust(rust_код, выходной, verbose=False):
    # Ищем rustc
    rustc = None
    for путь in ['rustc',
                 os.path.expanduser('~/.cargo/bin/rustc'),
                 r'C:\Users\%s\.cargo\bin\rustc.exe' % os.environ.get('USERNAME',''),
                 r'C:\Program Files\Rust\bin\rustc.exe']:
        путь = os.path.expandvars(путь)
        try:
            r = subprocess.run([путь, '--version'], capture_output=True)
            if r.returncode == 0:
                rustc = путь; break
        except FileNotFoundError:
            continue

    if not rustc:
        print('\033[31mОшибка:\033[0m rustc не найден. Установите Rust: https://rustup.rs', file=sys.stderr)
        return False

    with tempfile.NamedTemporaryFile(suffix='.rs', mode='w', delete=False, encoding='utf-8') as f:
        f.write(rust_код); rs_файл = f.name

    try:
        команда = [rustc, rs_файл, '-o', выходной,
                   '--edition', '2021',
                   '-C', 'opt-level=2',
                   '-A', 'warnings']
        if verbose:
            print(f'  rustc {rs_файл} -o {выходной}')
        рез = subprocess.run(команда, capture_output=True, text=True)
        if рез.returncode != 0:
            print(f'\033[31mОшибка компиляции Rust:\033[0m', file=sys.stderr)
            for строка in рез.stderr.split('\n'):
                if строка.strip():
                    print(f'  {строка}', file=sys.stderr)
            return False
        return True
    finally:
        os.unlink(rs_файл)


def главная():
    if len(sys.argv) < 2 or sys.argv[1] in ('-п','--помощь','-h','--help'):
        print(БАННЕР)
        print('Использование:')
        print('  сибиряк <файл.сбк>              скомпилировать')
        print('  сибиряк <файл.сбк> -о <имя>     с именем выходного файла')
        print('  сибиряк <файл.сбк> --rust        сохранить Rust-код')
        print('  сибиряк <файл.сбк> --токены      показать токены')
        print('  сибиряк <файл.сбк> --аст         показать АСД')
        print('  сибиряк запустить <файл.сбк>     скомпилировать и запустить')
        print('  сибиряк --версия                 версия компилятора')
        sys.exit(0)

    if sys.argv[1] in ('-в','--версия','--version'):
        print(f'Сибиряк {ВЕРСИЯ}  (бэкенд: Rust)')
        sys.exit(0)

    аргументы = sys.argv[1:]
    запустить = аргументы[0] == 'запустить'
    if запустить: аргументы = аргументы[1:]
    if not аргументы:
        print('Укажите файл .сбк', file=sys.stderr); sys.exit(1)

    имя_файла = аргументы[0]
    только_rust  = '--rust'   in аргументы
    показ_токенов= '--токены' in аргументы
    показ_аст    = '--аст'    in аргументы
    verbose      = '-v'       in аргументы or '--подробно' in аргументы

    выходной = None
    for i, а in enumerate(аргументы):
        if а in ('-о','--выход') and i+1 < len(аргументы):
            выходной = аргументы[i+1]; break
    if not выходной:
        base = os.path.splitext(имя_файла)[0]
        выходной = base + ('.exe' if sys.platform == 'win32' else '')

    try:
        with open(имя_файла, 'r', encoding='utf-8') as f:
            исходник = f.read()
    except FileNotFoundError:
        print(f'\033[31mФайл не найден:\033[0m {имя_файла}', file=sys.stderr); sys.exit(1)

    print(f'\033[36mСибиряк\033[0m  компилирует  \033[33m{имя_файла}\033[0m  →  Rust  →  \033[33m{выходной}\033[0m')

    токены = токенизировать(исходник, имя_файла)
    if показ_токенов:
        for т in токены:
            if т.тип.name != 'КОНЕЦ_ФАЙЛА':
                print(f'  \033[33m{т.тип.name:<25}\033[0m {т.значение!r}  стр:{т.строка}')

    аст = разобрать(токены, имя_файла)
    if показ_аст:
        print(f'\033[36mАСД:\033[0m {аст}')

    rust_код = сгенерировать_rust(аст, имя_файла)

    if только_rust:
        rs_имя = выходной.replace('.exe','') + '.rs'
        with open(rs_имя, 'w', encoding='utf-8') as f:
            f.write(rust_код)
        print(f'\033[32m✓\033[0m  Rust-код сохранён: \033[33m{rs_имя}\033[0m')
        sys.exit(0)

    if скомпилировать_rust(rust_код, выходной, verbose):
        print(f'\033[32m✓\033[0m  Готово: \033[33m{выходной}\033[0m')
        if запустить:
            бинарь = выходной if os.path.isabs(выходной) else './' + выходной
            if sys.platform == 'win32':
                бинарь = выходной
            print(f'\033[36m── Запуск ─────────────────────────────────────\033[0m')
            код = subprocess.run([бинарь]).returncode
            sys.exit(код)
    else:
        sys.exit(1)

if __name__ == '__main__':
    главная()

@echo off
chcp 65001 >nul
echo.
echo  ██████████████████████████████████████████
echo  ██   Установщик языка Сибиряк 0.2.0    ██
echo  ██████████████████████████████████████████
echo.

:: Проверяем Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [!] Python не найден!
    echo  [!] Скачайте Python 3.8+ с https://www.python.org/downloads/
    echo  [!] При установке отметьте "Add Python to PATH"
    echo.
    pause
    start https://www.python.org/downloads/
    exit /b 1
)

echo  [OK] Python найден
echo  Запускаем графический установщик...
echo.

:: Запускаем .pyw (pythonw — без консоли, python — с консолью как запасной вариант)
pythonw "%~dp0СибирякУстановщик-0.2.0.pyw" 2>nul
if %errorlevel% neq 0 (
    python "%~dp0СибирякУстановщик-0.2.0.pyw"
)

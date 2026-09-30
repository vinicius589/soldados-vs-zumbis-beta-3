@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if errorlevel 1 (
    set "SVZ_PYTHON=python"
) else (
    set "SVZ_PYTHON=py -3"
)

%SVZ_PYTHON% -c "import pygame, OpenGL, numpy" >nul 2>nul
if errorlevel 1 (
    echo Preparando Pygame e PyOpenGL. Isso acontece apenas na primeira abertura.
    %SVZ_PYTHON% -m pip install -r requirements.txt
    if errorlevel 1 goto :erro
)

%SVZ_PYTHON% main.py
if errorlevel 1 goto :erro
exit /b 0

:erro
echo.
echo O jogo encontrou um erro. Envie a mensagem acima para correcao.
pause
exit /b 1

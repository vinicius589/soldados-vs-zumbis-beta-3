@echo off
echo ===================================================
echo   Compilador do Jogo - Soldados vs Zumbis (Beta 1)
echo ===================================================
echo.
echo Este script vai gerar um arquivo executavel (.exe) do jogo.
echo O arquivo gerado podera ser executado em qualquer computador
echo Windows sem precisar instalar o Python ou o PyCharm!
echo.
pause

echo Instalando o PyInstaller (ferramenta de compilacao)...
python -m pip install pyinstaller

echo.
echo Compilando o jogo...
pyinstaller --noconfirm --onedir --windowed --name "Soldados vs Zumbis Beta 1" src/main.py

echo.
echo ===================================================
echo COMPILACAO CONCLUIDA!
echo ===================================================
echo O seu jogo pronto para ser distribuido esta na pasta:
echo dist\Soldados vs Zumbis Beta 1\
echo.
echo Basta copiar essa pasta inteira e enviar para seus amigos,
echo e eles so precisarao abrir o "Soldados vs Zumbis Beta 1.exe".
echo.
pause

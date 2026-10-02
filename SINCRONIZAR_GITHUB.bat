@echo off
echo ===================================================
echo   Sincronizacao com o GitHub - Beta 1
echo ===================================================
echo.
echo Este script vai inicializar o versionamento do projeto
echo local e envia-lo para o repositorio Beta 4 no GitHub.
echo.
pause

echo Inicializando repositorio Git...
git init
git config user.name "Vinicius"
git config user.email "vinicius589@users.noreply.github.com"
git add .
git commit -m "feat: integracao da Beta 1 ao historico do projeto"

echo.
echo Conectando ao repositorio remoto...
git remote add origin https://github.com/vinicius589/soldados-vs-zumbis-beta-4.git

echo.
echo Criando branch separada para o historico da Beta 1...
git checkout -b historico/beta-1

echo.
echo Enviando para o GitHub...
git push -u origin historico/beta-1

echo.
echo ===================================================
echo CONCLUIDO! 
echo ===================================================
echo A sua Beta 1 foi enviada para o GitHub numa branch chamada 'historico/beta-1'.
echo Agora voce pode acessar o GitHub e criar um Pull Request para unir (merge)
echo as versoes se desejar, ou apenas mante-la preservada no historico!
echo.
pause

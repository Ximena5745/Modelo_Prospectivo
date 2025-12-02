@echo off
echo ============================================================
echo  GENERADOR DE PDF CONSOLIDADO - INDICADORES Y MODELOS
echo  Politecnico Grancolombiano - Plataforma Prospectiva
echo ============================================================
echo.
echo Iniciando generacion del PDF consolidado...
echo.

REM Activar entorno virtual si existe
if exist ".\Scripts\activate.bat" (
    echo Activando entorno virtual...
    call .\Scripts\activate.bat
)

REM Ejecutar el generador
python generar_pdf_consolidado.py

echo.
echo ============================================================
echo Proceso finalizado.
echo ============================================================
echo.
pause

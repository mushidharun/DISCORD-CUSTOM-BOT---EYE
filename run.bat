# =========================================================
#  ZETRA DISCORD BUSINESS BOT – COMMERCIAL EDITION
#  COPYRIGHT OWNER : MUSHI DHARUN (ZETRA)
#  PRICE : DM ME DIRECTLY OR CONTACT IN MY SERVER
#  SERVER : https://discord.gg/uxMjPz749k
#
#  This software is proprietary and confidential.
#  Unauthorized copying, modification, resale,
#  redistribution, or sharing is strictly prohibited.
# =========================================================

@echo off
title BLUE EYE • AUTO RESTART 👁️
color 0B

:loop
cls
echo =========================================
echo        BLUE EYE STARTING...
echo        ZETRA IS WATCHING YOU 👁️
echo        %date% %time%
echo =========================================

python main.py

echo.
echo =========================================
echo BOT STOPPED OR CRASHED
echo Restarting in 5 seconds...
echo %date% %time%
echo =========================================

timeout /t 5 >nul
goto loop

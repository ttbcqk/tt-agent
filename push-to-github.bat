@echo off
cd /d "C:\Users\48548\WorkBuddy\2026-11-21-21-12-29\tt-agent"
title Push Agent to GitHub
set GIT="C:\Users\48548\.workbuddy\vendor\PortableGit\cmd\git.exe"
echo ============================================
echo   Push Travel Agent to GitHub
echo ============================================
echo.
echo If a GitHub login window pops up, please sign in with ttbcqk.
echo If "Select a credential helper" appears, choose manager.
echo Retrying up to 20 times.
echo.
set /a n=0
:retry
set /a n+=1
echo ------ Attempt %n% ------
%GIT% -c credential.helper=manager push origin main
if %ERRORLEVEL% EQU 0 goto ok
if %n% GEQ 20 goto fail
timeout /t 3 >nul
goto retry
:ok
echo.
echo [SUCCESS] Code pushed! Makers will auto-redeploy in 1-3 minutes.
echo Refresh the preview link to see the new Agent.
goto end
:fail
echo.
echo [FAILED] Could not push. Check your network / GitHub login.
:end
echo.
pause

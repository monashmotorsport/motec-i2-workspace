@echo off
setlocal enabledelayedexpansion

:: --- CONFIGURATION ---
:: Replace this URL with your actual repository ZIP download link
set "REPO_ZIP_URL=https://github.com/monashmotorsport/motec-i2-workspace/archive/refs/heads/main.zip"
set "TEMP_ZIP=%TEMP%\motec_update.zip"
set "TEMP_EXTRACT=%TEMP%\motec_temp_extract"

:: Base path is where the .bat file is currently sitting
set "BASE_DIR=%~dp0"
set "TARGET_CHANNELS=%BASE_DIR%Channels"
set "TARGET_MATHS=%BASE_DIR%Maths"

echo ===========================================
echo   MoTeC Standard Standards Sync
echo ===========================================
echo Workspace Location: "%BASE_DIR%"
echo.

:: Check if MoTeC i2 Pro is running
echo Checking MoTeC status...
tasklist | find /i "i2.exe" >nul
if %errorlevel% equ 0 (
    echo.
    echo ===========================================
    echo  [!] ERROR: MoTeC i2 Pro is currently open!
    echo ===========================================
    echo Please save your work and close i2 completely.
    echo Running this script while i2 is open will cause data loss.
    echo.
    pause
    exit /b
)

:: 1. Download the ZIP
echo [1/4] Downloading latest updates...
powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%REPO_ZIP_URL%' -OutFile '%TEMP_ZIP%'"

:: 2. Extract the ZIP
echo [2/4] Extracting files...
if exist "%TEMP_EXTRACT%" rmdir /s /q "%TEMP_EXTRACT%"
powershell -Command "Expand-Archive -Path '%TEMP_ZIP%' -DestinationPath '%TEMP_EXTRACT%'"

:: 3. Identify the extracted folder (GitHub adds branch name to the folder)
for /d %%i in ("%TEMP_EXTRACT%\*") do set "ROOT_FOLDER=%%i"

:: 4. Update Aliases.xml
echo [3/4] Updating Channels/Aliases.xml...
if exist "%ROOT_FOLDER%\Channels\Aliases.xml" (
    copy /y "%ROOT_FOLDER%\Channels\Aliases.xml" "%TARGET_CHANNELS%\Aliases.xml" >nul
    echo      - Successfully updated Aliases.xml
) else (
    echo      [!] WARNING: Aliases.xml not found in repository.
)

:: 5. Update Maths Folder and Echo filenames
echo [4/4] Updating Math Channels...
if exist "%ROOT_FOLDER%\Maths" (
    for %%f in ("%ROOT_FOLDER%\Maths\*.xml") do (
        copy /y "%%f" "%TARGET_MATHS%\" >nul
        echo      + Updated: %%~nxf
    )
) else (
    echo      [!] WARNING: Maths folder not found in repository.
)

:: 6. Cleanup
echo.
echo Cleaning up temporary files...
del "%TEMP_ZIP%"
rmdir /s /q "%TEMP_EXTRACT%"

echo.
echo ===========================================
echo   SUCCESS: Workspace is now up to date.
echo ===========================================
pause
@echo off
echo Cleaning up previous builds...

:: Delete the old .exe if it exists
if exist "dist\frog_game.exe" (
    del /f "dist\frog_game.exe"
    echo Old .exe file deleted.
) else (
    echo No previous .exe file found.
)

:: Delete the build folder
if exist "build" (
    rmdir /s /q "build"
    echo Build folder cleaned.
)

:: Run PyInstaller to rebuild the project
echo Rebuilding the project...
pyinstaller --onefile --windowed frog_game.py

:: Pause to see the output
pause

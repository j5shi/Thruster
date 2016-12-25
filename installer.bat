@echo off

taskkill /IM Launchy.exe /F

xcopy /E /Y pylibs  "%programfiles(x86)%\Launchy" 
xcopy /E /Y plugins "%programfiles(x86)%\Launchy\plugins"

echo **************************************************************************
echo * Thruster has been installed successfully!                              * 
echo **************************************************************************
pause 
start "" /D "%programfiles(x86)%\Launchy"  "Launchy.exe"

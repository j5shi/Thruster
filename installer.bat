@echo off

taskkill /IM Launchy.exe /F

xcopy /E /Y pylibs  "%programfiles(x86)%\Launchy" 
xcopy /E /Y plugins "%programfiles(x86)%\Launchy\plugins"

echo **************************************************
echo * Thruster has been installed successfully,      * 
echo * please restart Launchy and rebuild the catalog *
echo **************************************************
pause 

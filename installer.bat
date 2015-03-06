@echo off

taskkill /IM Launchy.exe /F

xcopy /Y boost_python-vc80-mt-1_41.dll "%programfiles(x86)%\Launchy"

xcopy /E /Y plugins "%programfiles(x86)%\Launchy\plugins"

echo **************************************************
echo * PyUltima has been installed successfully,      * 
echo * please restart Launchy and rebuild the catalog *
echo **************************************************
pause 

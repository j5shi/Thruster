@echo off

xcopy /Y boost_python-vc80-mt-1_41.dll "%programfiles(x86)%\Launchy"

xcopy /E /Y plugins "%programfiles(x86)%\Launchy\plugins"

echo "BookmarkMgr has been installed successfully, please restart Launchy and build the catalog."
pause 

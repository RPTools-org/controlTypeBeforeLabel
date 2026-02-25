;@echo off
title Build controlTypeBeforeLabel 

call scons -s
SET /P PR=Press Enter to continue...
move *.nvda-addon ..
call scons -c
del /s /q *.pyc > NUL
del .sconsign.dblite> NUL
rd /s  /q __pycache__
rd /s /q  .\site_scons\site_tools\gettexttool\__pycache__


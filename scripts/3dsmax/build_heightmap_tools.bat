@ECHO ON
SET SourceDir=%~dp0
SET DestDir=%~dp0
CD /D "C:\Program Files\7-Zip"
7z.exe a -tzip "%DestDir%\mzp\ht_tools.mzp" "%SourceDir%\lib" "%SourceDir%\icons\ht" "%SourceDir%\ht_tools\*" "%SourceDir%\raw*.ms" "%SourceDir%\settings.ini" -mx5
EXIT
@ECHO ON
SET SourceDir=%~dp0
SET DestDir=%~dp0
CD /D "C:\Program Files\7-Zip"
7z.exe a "%DestDir%\ht_tool.zip" "%SourceDir%\*" -mx5 -x!*.bat
ren %DestDir%\ht_tool.zip ht_tool.mzp
EXIT
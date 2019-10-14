@ECHO ON
SET SourceDir=%~dp0
SET DestDir=%~dp0
CD /D "C:\Program Files\7-Zip"
7z.exe a -tzip "%DestDir%\ht_tools.zip" "%SourceDir%\*" -mx5 -x!*.bat -x!*.md
EXIT
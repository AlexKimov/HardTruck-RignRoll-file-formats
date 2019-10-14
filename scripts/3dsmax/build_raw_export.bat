call "run_raw_export.bat"

SET SourceDir=%~dp0
SET DestDir=%~dp0
CD /D "C:\Program Files\7-Zip"
7z.exe a -tzip "%DestDir%\builds\raw_export.zip" "%SourceDir%\builds\raw_export.ms" "%SourceDir%\builds\raw_export_settings.ini" "%SourceDir%\builds\raw_export_strings.ini" -mx5
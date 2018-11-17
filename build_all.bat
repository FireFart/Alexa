@echo off

call :runBuild decision
call :runBuild dnslookup
call :runBuild percentage
call :runBuild randomnumber

goto :eof

:runBuild
echo Building %~1
cd %~1
call .\build.bat
cd..
goto :eof
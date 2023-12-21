@echo off
color 0A

if exist "%ProgramFiles%\Microsoft Office\Office16\ospp.vbs" (
    cd /d "%ProgramFiles%\Microsoft Office\Office16"
)

if exist "%ProgramFiles(x86)%\Microsoft Office\Office16\ospp.vbs" (
    cd /d "%ProgramFiles(x86)%\Microsoft Office\Office16"
)

echo ############################## Tool Da Năng  #####################################
echo #                                                                                #
echo #                            www.ketcaumkpr.id.vn                                #
echo #                                                                                #
echo ##################################################################################
echo ############################## INFO  #############################################
echo #                                                                                #
echo #                        SDT:0867544809 Code By Minh Khoa                        #
echo #                                                                                #
echo ##################################################################################

cscript.exe OSPP.vbs /dstatus
set /p activateAgain=Do you want to activate the license again? (Y/N):

if /i "%activateAgain%"=="Y" (
    powershell.exe -command "& { irm https://massgrave.dev/get | iex }"
)
pause

pause

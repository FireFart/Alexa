@echo off

rmdir /S /Q skill
pip install -r requirements.txt -t skill/
pip install --user babel
pybabel extract data.py -o locales/base.pot
pybabel update -i locales/base.pot -d locales
pybabel compile -d locales
xcopy locales skill\locales /e /i /h /y
copy /Y *.py skill\
del /f percentage.zip
"C:\Program Files\7-Zip\7z.exe" a -r percentage.zip -w .\skill\* -mem=AES256

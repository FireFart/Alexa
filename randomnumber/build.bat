@echo off

rmdir /S /Q skill
pip install -r requirements.txt -t skill/ --upgrade
pip install --user babel --upgrade
pybabel extract data.py -o locales/base.pot
pybabel update -i locales/base.pot -d locales
pybabel compile -d locales
xcopy locales skill\locales /e /i /h /y
copy /Y *.py skill\
del /f random.zip
"C:\Program Files\7-Zip\7z.exe" a -r random.zip -w .\skill\* -mem=AES256
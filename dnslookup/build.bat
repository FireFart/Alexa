@echo off

mkdir skill
pip install -r requirements.txt -t skill/
copy /Y lambda_function.py skill/lambda_function.py
del /f dnslookup.zip
"C:\Program Files\7-Zip\7z.exe" a -r dnslookup.zip -w .\skill\* -mem=AES256
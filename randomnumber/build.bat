@echo off

mkdir skill
pip install -r requirements.txt -t skill/
copy /Y lambda_function.py skill/lambda_function.py
del /f random.zip
"C:\Program Files\7-Zip\7z.exe" a -r random.zip -w .\skill\* -mem=AES256
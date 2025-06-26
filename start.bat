@echo off

:: Create uploads directory if it doesn't exist
if not exist uploads mkdir uploads

:: Start the application
gunicorn --config gunicorn_config.py app:app

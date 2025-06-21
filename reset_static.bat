@echo off
echo Cleaning static files...
if exist staticfiles\ (
    rmdir /s /q staticfiles
    echo Removed staticfiles directory
) else (
    echo No staticfiles directory found
)

echo.
echo Collecting static files...
python manage.py collectstatic --noinput

echo.
echo Done! Now restart your Django server.

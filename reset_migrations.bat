@echo off
echo Resetting problematic migrations...

rem First, fake apply all migrations to get to a clean state
python manage.py migrate --fake

rem Remove migration files except __init__.py for problematic apps
cd apps\accounts\migrations
del /Q 00*.py
echo. > __init__.py
cd ..\..\standards\migrations
del /Q 00*.py
echo. > __init__.py
cd ..\..\company\migrations
del /Q 00*.py 
echo. > __init__.py
cd ..\..

rem Create fresh migrations
python manage.py makemigrations accounts standards company

rem Fake apply the new initial migrations
python manage.py migrate --fake-initial

echo Migration reset complete.

echo yes | python manage.py collectstatic
git add .
git commit -m "auto submit"
git push $1 $2:1

python3 generatesite.py
python3 generatesite.py templates/template_dark.txt dark
python3 generatesite.py templates/template_nocss.txt nocss

cp -r output/* /var/www

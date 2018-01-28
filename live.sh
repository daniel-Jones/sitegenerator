python3 generatesite.py
python3 generatesite.py templates/template_dark.txt dark
python3 generatesite.py templates/template_nocss.txt nocss
python3 generatesite.py templates/template_kawaii.txt kawaii
cp -r output/* /var/www

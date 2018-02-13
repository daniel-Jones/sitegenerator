python3 generatesite.py
python3 generatesite.py templates/template_dark.txt dark
python3 generatesite.py templates/template_nocss.txt nocss
python3 generatesite.py templates/template_kawaii.txt kawaii
cp -r output/* /var/www
chmod -R +r /var/www/blog
chmod -R +r /var/www/dark
chmod -R +r /var/www/kawaii
chmod -R +r /var/www/nocss

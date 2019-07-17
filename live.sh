python3 generatesite.py
python3 generatesite.py templates/template_dark.txt dark
python3 generatesite.py templates/template_nocss.txt nocss
python3 generatesite.py templates/template_kawaii.txt kawaii
python3 generatesite.py templates/template_light.txt light
python3 generatesite.py templates/template_solarized.txt solarized 
cp -r output/* /var/www/html
chmod -R +r /var/www/html/blog
chmod -R +r /var/www/html/posts
chmod -R +r /var/www/html/dark
chmod -R +r /var/www/html/kawaii
chmod -R +r /var/www/html/nocss
chmod -R +r /var/www/html/light
chmod -R +r /var/www/html/solarized

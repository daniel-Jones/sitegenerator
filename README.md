# sitegenerator
static site generator for my website/blog/portfolio at https://danieljon.es
# why?
My website previously relied heavily on php/databases and didn't render correctly inside my terminal web browser so I decided to take the static, html only route and created a static website generator.
# how do I use it?
I've created the setup.sh script, it will generate everything you need to get a minimal website up with a few example blog posts, anime recommendation of k-on, nico as your waifu and two sample projects in your portfolio. 
'''
Run ./setup.sh once.
then everytime you update the site run:
python3 generatesite.py && cp -r output/* /var/www #or where ever your root dir is
'''
# settings.cfg?
This file contains various settings you can change including the number of blog posts per page, titles, content locations, blog directory etc. Play with these if you want.

# .htaccess for blog?
I use the following as my .htaccees for /blog, it makes /blog go to blog/1, /1 translates to 1.html etc:

```
Options +SymLinksIfOwnerMatch
Order Allow,Deny
Allow from all
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^([A-Za-z0-9-]+)/?$ $1.html [NC,QSA]
DirectoryIndex 1.html
```

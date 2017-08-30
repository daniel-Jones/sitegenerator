# sitegenerator
static site generator for my website/blog/portfolio at https://danieljon.es
# why?
My website previously relied heavily on php/databases and didn't render correctly inside my terminal web browser so I decided to take the static, html only route and created a static website generator.
# how do I use it?
This script is really _really_ optimised for _my_ setup. to use it in its default state you need to do the following:

modify template.txt to your liking, this is used on EVERY page

create a directory named content

create content/index.txt, this will hold your index.html content (just text and stuff)

create content/portfolio.txt (or remove generateportfolio();)

create directory content/blog

create blog posts in content/blog, 1.txt is the OLDEST post.

It's all just .txt files, you can add html/js to them.

# settigns.cfg?
This file contains various settings you cna change including the number of blog posts per page, titles, content locations, blog directory etc. Play with these if you want.

#.htaccess for blog?
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

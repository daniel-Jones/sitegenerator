# sync all the media directories, this only has to be run when new media is added

# root media directory
rsync -r /var/www/media /var/www/kawaii/
rsync -r /var/www/media /var/www/dark/
rsync -r /var/www/media /var/www/light/
rsync -r /var/www/media /var/www/nocss/
rsync -r /var/www/media /var/www/solarized/

# blog media directory
rsync -r /var/www/blog/media /var/www/kawaii/blog/
rsync -r /var/www/blog/media /var/www/dark/blog/
rsync -r /var/www/blog/media /var/www/light/blog/
rsync -r /var/www/blog/media /var/www/nocss/blog/
rsync -r /var/www/blog/media /var/www/solarized/blog/

# waifu media directory
rsync -r /var/www/waifus/media /var/www/kawaii/waifus/
rsync -r /var/www/waifus/media /var/www/dark/waifus/
rsync -r /var/www/waifus/media /var/www/light/waifus/
rsync -r /var/www/waifus/media /var/www/nocss/waifus/
rsync -r /var/www/waifus/media /var/www/solarized/waifus/

# opinions media directory
rsync -r /var/www/opinions/media /var/www/kawaii/opinions/
rsync -r /var/www/opinions/media /var/www/dark/opinions/
rsync -r /var/www/opinions/media /var/www/light/opinions/
rsync -r /var/www/opinions/media /var/www/nocss/opinions/
rsync -r /var/www/opinions/media /var/www/solarized/opinions/

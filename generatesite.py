#!/usr/bin/env python3

'''
script to auto-generate my static website/blog/portfolio @ https://danieljon.es
'''

import configparser;
import errno;
import os;
import glob;
from shutil import copyfile;
from tempfile import mkstemp;
from shutil import move;
from os import fdopen, remove;
from time import gmtime, strftime;

def replace(file_path, pattern, subst):
    fh, abs_path = mkstemp();
    with fdopen(fh, "w") as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst));
    remove(file_path);
    move(abs_path, file_path);

def generateindex():
    template = cfg.get("output", "template");
    outdir = cfg.get("output", "dir");
    indexsrc = cfg.get("index", "src");
    print("generating {}/index.html from {}".format(outdir, indexsrc));
    copyfile(template, outdir + "/index.html");
    with open(indexsrc, "r") as contentfile:
        content = contentfile.read();
    replace(outdir + "/index.html", "{TITLE}", cfg.get("index", "title"));
    replace(outdir + "/index.html", "{INFO}", cfg.get("index", "header"));
    replace(outdir + "/index.html", "{CONTENT}", content);
    replace(outdir + "/index.html", "{TIME}", strftime("%Y-%m-%d %H:%M:%S", gmtime()));

def generatepagebar(currentpage, pagecount):
    print("generating page bar for {} total {}".format(currentpage, pagecount));
    pages = "<div class='middle'> <a href='" + str(pagecount if int(currentpage) == 1 else int(currentpage)-1) + "'>prev</a> ";
    for x in range(1, int(pagecount)+1):
        if x == int(currentpage):
            pages += "<strong><i><a href=" + str(x) + ">" + str(x) + "</a></i></strong> ";
        else: 
            pages += "<a href=" + str(x) + ">" + str(x) + "</a> ";
    pages += "<a href='" + str(1 if currentpage == pagecount else int(currentpage)+1) + "'>next</a></div>";
    return pages;

def generateportfolio():
    template = cfg.get("output", "template");
    outdir = cfg.get("output", "dir");
    portfoliosrc = cfg.get("portfolio", "src");
    print("generating {}/portfolio.html from {}".format(outdir, portfoliosrc));
    copyfile(template, outdir + "/portfolio.html");
    with open(portfoliosrc, "r") as contentfile:
        content = contentfile.read();
    replace(outdir + "/portfolio.html", "{TITLE}", cfg.get("portfolio", "title"));
    replace(outdir + "/portfolio.html", "{INFO}", cfg.get("portfolio", "header"));
    replace(outdir + "/portfolio.html", "{CONTENT}", content);
    replace(outdir + "/portfolio.html", "{TIME}", strftime("%Y-%m-%d %H:%M:%S", gmtime()));

def deletefiles(ddir):
     # delete all blog files
    for the_file in os.listdir(ddir):
        file_path = os.path.join(ddir, the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path);

def generateblog():
    template = cfg.get("output", "template");
    outdir = cfg.get("output", "dir");
    blogdir = cfg.get("blog", "dir");
    directdir = cfg.get("blog", "direct");
    blogsrc = cfg.get("blog", "srcdir");
    perpage = cfg.get("blog", "perpage");
    print("generating {}/{}/ from directory /{}/final".format(outdir, blogdir, blogsrc));
    os.makedirs(outdir + "/" + blogdir, exist_ok=True);
    os.makedirs(outdir + "/" + blogdir + "/" + directdir, exist_ok=True);
    os.makedirs(blogsrc + "/final", exist_ok=True);
   # number of blog posts
    postcount = len(glob.glob1(blogsrc, "*.txt"));
    pagecount = postcount/int(perpage)+1;
    print("{} posts, {} per page = {} pages".format(postcount, perpage, int(pagecount)));
    folder = outdir + "/" + blogdir;
    # delete generated blog files
    deletefiles(outdir + "/" + blogdir);
    # delete renamed blog files
    deletefiles(blogsrc + "/final");
    '''
    copy our blog posts to blogsrc/final, rename them, 60 becomes 1, 59 becomes 2 etc
    this is done because I am extremely lazy and had troubles doing it any other way.
    sorry if you're reading this.
    '''
    #integrate this with the loop below it?
    count = 1;
    for x in range(int(postcount), 0, -1):
        copyfile(blogsrc + "/" + str(x) + ".txt", blogsrc + "/final/" + str(count) + ".txt");
        count += 1;
    # generate pages
    for x in range(1, int(pagecount) + 1):
        copyfile(template, outdir + "/" + blogdir + "/" + str(x) + ".html");
        with open(outdir + "/" + blogdir + "/" + str(x) + ".html", "r") as contentfile:
            content = contentfile.read().replace('\n', '');
        replace(outdir + "/" + blogdir + "/" + str(x) + ".html", "{TITLE}", cfg.get("blog", "title"));
        replace(outdir + "/" + blogdir + "/" + str(x) + ".html", "{INFO}", cfg.get("blog", "header"));
        replace(outdir + "/" + blogdir + "/" + str(x) + ".html", "{TIME}", strftime("%Y-%m-%d %H:%M:%S", gmtime()));
    # place blog posts into their pages
    count = 1;
    cpage = 1;
    page = "";
    total_count = postcount;
    # count from 1 - perpage, add perpage to count, count from count - count + perpage
    while count < postcount + 1:
        for x in range(count, count + int(perpage)):
            if count < postcount + 1:
                with open(blogsrc + "/final/" + str(x) + ".txt") as contentfile:
                    content = contentfile.read();
                    page += "<div id='" + str(total_count) + "'> <a href='" + directdir + "/" + str(total_count) + "'>direct link</a>" + content + "</div><hr>";
                    count += 1;
                    total_count -= 1;
        if cpage <= pagecount:
            page += generatepagebar(str(cpage), str(int(pagecount)));
            page = generatepagebar(str(cpage), str(int(pagecount))) + page;
            replace(outdir + "/" + blogdir + "/" + str(cpage) + ".html", "{CONTENT}", page);
        page = "";
        cpage += 1;
    # generate /direct/ pages
    for x in range(1, int(postcount) + 1):
        copyfile(template, outdir + "/" + blogdir + "/" + directdir + "/" + str(x) + ".html");
        replace(outdir + "/" + blogdir + "/" + directdir + "/" + str(x) + ".html", "{TITLE}", cfg.get("blog", "title"));
        replace(outdir + "/" + blogdir + "/" + directdir + "/" + str(x) + ".html", "{INFO}", cfg.get("blog", "header"));
        replace(outdir + "/" + blogdir + "/" + directdir + "/" + str(x) + ".html", "{TIME}", strftime("%Y-%m-%d %H:%M:%S", gmtime()));
        with open(blogsrc + "/" + str(x) + ".txt") as contentfile:
            content = contentfile.read();
            replace(outdir + "/" + blogdir + "/" + directdir + "/" + str(x) + ".html", "{CONTENT}", content);
            replace(outdir + "/" + blogdir + "/" + directdir + "/" + str(x) + ".html", "media/", "../media/");




def generateanime():
    template = cfg.get("output", "template");
    outdir = cfg.get("output", "dir");
    animesrc = cfg.get("anime", "src");
    animedir = cfg.get("anime", "dir");
    print("generating {}/{}/index.html from {}".format(outdir, animedir, animesrc));
    copyfile(template, outdir + "/" + animedir + "/index.html");
    with open(animesrc, "r") as contentfile:
        content = contentfile.read();
    replace(outdir + "/" + animedir + "/index.html", "{TITLE}", cfg.get("anime", "title"));
    replace(outdir + "/" + animedir + "/index.html", "{INFO}", cfg.get("anime", "header"));
    replace(outdir + "/" + animedir + "/index.html", "{CONTENT}", content);
    replace(outdir + "/" + animedir + "/index.html", "{TIME}", strftime("%Y-%m-%d %H:%M:%S", gmtime()));

def generatewaifus():
    template = cfg.get("output", "template");
    outdir = cfg.get("output", "dir");
    waifussrc = cfg.get("waifus", "src");
    waifusdir = cfg.get("waifus", "dir");
    print("generating {}/{}/index.html from {}".format(outdir, waifusdir, waifussrc));
    copyfile(template, outdir + "/" + waifusdir + "/index.html");
    with open(waifussrc, "r") as contentfile:
        content = contentfile.read();
    replace(outdir + "/" + waifusdir + "/index.html", "{TITLE}", cfg.get("waifus", "title"));
    replace(outdir + "/" + waifusdir + "/index.html", "{INFO}", cfg.get("waifus", "header"));
    replace(outdir + "/" + waifusdir + "/index.html", "{CONTENT}", content);
    replace(outdir + "/" + waifusdir + "/index.html", "{TIME}", strftime("%Y-%m-%d %H:%M:%S", gmtime()));

if __name__ == "__main__":
    cfg = configparser.ConfigParser();
    cfg.read("settings.cfg");
    os.makedirs(cfg.get("output", "dir"), exist_ok=True);
    generateindex(); # index
    generateblog(); # blog with individual pages
    generateportfolio(); # portfolio
    generateanime(); # anime recommendations
    generatewaifus(); # my waifus

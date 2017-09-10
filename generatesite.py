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
        content = contentfile.read().replace('\n', '');
    replace(outdir + "/index.html", "{TITLE}", cfg.get("index", "title"));
    replace(outdir + "/index.html", "{INFO}", cfg.get("index", "header"));
    replace(outdir + "/index.html", "{CONTENT}", content);
    replace(outdir + "/index.html", "{TIME}", strftime("%Y-%m-%d %H:%M:%S", gmtime()));

def generatepagebar(currentpage, pagecount):
    print("generating page bar for {} total {}".format(currentpage, pagecount));
    pages = "<center>page ";
    for x in range(1, int(pagecount)+1):
        if x == int(currentpage):
            pages += "<strong><i><a href=" + str(x) + ">" + str(x) + "</a></i></strong> ";
        else: 
            pages += "<a href=" + str(x) + ">" + str(x) + "</a> ";
    pages += "</center>";
    return pages;

def generateportfolio():
    template = cfg.get("output", "template");
    outdir = cfg.get("output", "dir");
    portfoliosrc = cfg.get("portfolio", "src");
    print("generating {}/portfolio.html from {}".format(outdir, portfoliosrc));
    copyfile(template, outdir + "/portfolio.html");
    with open(portfoliosrc, "r") as contentfile:
        content = contentfile.read().replace('\n', '');
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
    blogsrc = cfg.get("blog", "srcdir");
    perpage = cfg.get("blog", "perpage");
    print("generating {}/{}/ from directory /{}/final".format(outdir, blogdir, blogsrc));
    os.makedirs(outdir + "/" + blogdir, exist_ok=True);
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
                    page += "#" + str(total_count) + content + "<hr>";
                    count += 1;
                    total_count -= 1;
        if cpage <= pagecount:
            page += generatepagebar(str(cpage), str(int(pagecount)));
            page = generatepagebar(str(cpage), str(int(pagecount))) + page;
            replace(outdir + "/" + blogdir + "/" + str(cpage) + ".html", "{CONTENT}", page);
        page = "";
        cpage += 1;
    '''
    for x in range(1, postcount + 1):
        with open(blogsrc + "/" + str(x) + ".txt", "r") as t:
            print(t.read());
    '''

if __name__ == "__main__":
    cfg = configparser.ConfigParser();
    cfg.read("settings.cfg");
    os.makedirs(cfg.get("output", "dir"), exist_ok=True);
    generateindex();
    generateblog();
    generateportfolio();

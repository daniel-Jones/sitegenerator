#!/usr/bin/env python3
'''
Copyright Daniel Jones daniel@danieljon.es

script to auto-generate my static website/blog at https://danieljon.es

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import configparser;
import errno;
import os;
import glob;
import sys;
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

def generateindex(special):
    if special:
        outdir = specialoutput;
    else:
        outdir = cfg.get("output", "dir");
    indexsrc = cfg.get("index", "src");
    print("generating {}/index.html from {}".format(outdir, indexsrc));
    copyfile(template, outdir + "/index.html");
    with open(indexsrc, "r") as contentfile:
        content = contentfile.read();
    replace(outdir + "/index.html", "{TITLE}", cfg.get("index", "title"));
    replace(outdir + "/index.html", "{INFO}", cfg.get("index", "header"));
    replace(outdir + "/index.html", "{CONTENT}", content);
    replace(outdir + "/index.html", "{TIME}", strftime("%d-%m-%Y", gmtime()));

def generatepagebar(currentpage, pagecount):
    print("generating page bar for {} total {}".format(currentpage, pagecount));
    pages = "<div class='middle'> <a href='" + str(pagecount if int(currentpage) == 1 else int(currentpage)-1) + "'>prev</a> ";
    for x in range(1, int(pagecount)+1):
        if x == int(currentpage):
            pages += "<strong><i>" + str(x) + "</i></strong> ";
        else: 
            pages += "<a href=" + str(x) + ">" + str(x) + "</a> ";
    pages += "<a href='" + str(1 if currentpage == pagecount else int(currentpage)+1) + "'>next</a></div>";
    return pages;

def generateportfolio(special):
    if special:
        outdir = specialoutput;
    else:
       outdir = cfg.get("output", "dir");
    portfoliosrc = cfg.get("portfolio", "src");
    print("generating {}/portfolio.html from {}".format(outdir, portfoliosrc));
    copyfile(template, outdir + "/portfolio.html");
    with open(portfoliosrc, "r") as contentfile:
        content = contentfile.read();
    replace(outdir + "/portfolio.html", "{TITLE}", cfg.get("portfolio", "title"));
    replace(outdir + "/portfolio.html", "{INFO}", cfg.get("portfolio", "header"));
    replace(outdir + "/portfolio.html", "{CONTENT}", content);
    replace(outdir + "/portfolio.html", "{TIME}", strftime("%d-%m-%Y", gmtime()));

def deletefiles(ddir):
     # delete all blog files
    for the_file in os.listdir(ddir):
        file_path = os.path.join(ddir, the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path);

def generateblog(special):
    if special:
        outdir = specialoutput;
    else:
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
        replace(outdir + "/" + blogdir + "/" + str(x) + ".html", "{TIME}", strftime("%d-%m-%Y", gmtime()));
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
                    postnum = str((postcount+1)-x);
                    if postnum == "101":
                        postnum = "5";
                    page += "<div id='" + str(total_count) + "'> post #" + postnum + "<br><a href='" + directdir + "/" + str(total_count) + "'>direct link</a>" + content + "</div><hr>";
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
        replace(outdir + "/" + blogdir + "/" + directdir + "/" + str(x) + ".html", "{TIME}", strftime("%d-%m-%Y %H:%M:%S", gmtime()));
        with open(blogsrc + "/" + str(x) + ".txt") as contentfile:
            content = contentfile.read();
            replace(outdir + "/" + blogdir + "/" + directdir + "/" + str(x) + ".html", "{CONTENT}", content);
            replace(outdir + "/" + blogdir + "/" + directdir + "/" + str(x) + ".html", "media/", "../media/");




def generateopinions(special):
    if special:
        outdir = specialoutput;
    else:
        outdir = cfg.get("output", "dir");
    opinionssrc = cfg.get("opinions", "src");
    opinionsdir = cfg.get("opinions", "dir");
    os.makedirs(outdir + "/" + opinionsdir, exist_ok=True);
    print("generating {}/{}/index.html from {}".format(outdir, opinionsdir, opinionssrc));
    copyfile(template, outdir + "/" + opinionsdir + "/index.html");
    with open(opinionssrc, "r") as contentfile:
        content = contentfile.read();
    replace(outdir + "/" + opinionsdir + "/index.html", "{TITLE}", cfg.get("opinions", "title"));
    replace(outdir + "/" + opinionsdir + "/index.html", "{INFO}", cfg.get("opinions", "header"));
    replace(outdir + "/" + opinionsdir + "/index.html", "{CONTENT}", content);
    replace(outdir + "/" + opinionsdir + "/index.html", "{TIME}", strftime("%d-%m-%Y", gmtime()));
    # anime
    animesrc = cfg.get("anime", "src");
    print("generating {}/{}/index.html from {}".format(outdir, opinionsdir, animesrc));
    copyfile(template, outdir + "/" + opinionsdir + "/anime.html");
    with open(animesrc, "r") as contentfile:
        content = contentfile.read();
    replace(outdir + "/" + opinionsdir + "/anime.html", "{TITLE}", cfg.get("anime", "title"));
    replace(outdir + "/" + opinionsdir + "/anime.html", "{INFO}", cfg.get("anime", "header"));
    replace(outdir + "/" + opinionsdir + "/anime.html", "{CONTENT}", content);
    replace(outdir + "/" + opinionsdir + "/anime.html", "{TIME}", strftime("%d-%m-%Y", gmtime()));
    #everything else
    everythingsrc = cfg.get("everything", "src");
    print("generating {}/{}/index.html from {}".format(outdir, opinionsdir, everythingsrc));
    copyfile(template, outdir + "/" + opinionsdir + "/everything.html");
    with open(everythingsrc, "r") as contentfile:
        content = contentfile.read();
    replace(outdir + "/" + opinionsdir + "/everything.html", "{TITLE}", cfg.get("everything", "title"));
    replace(outdir + "/" + opinionsdir + "/everything.html", "{INFO}", cfg.get("everything", "header"));
    replace(outdir + "/" + opinionsdir + "/everything.html", "{CONTENT}", content);
    replace(outdir + "/" + opinionsdir + "/everything.html", "{TIME}", strftime("%d-%m-%Y", gmtime()));


def generatewaifus(special):
    if special:
        outdir = specialoutput;
    else:
        outdir = cfg.get("output", "dir");
    waifussrc = cfg.get("waifus", "src");
    waifusdir = cfg.get("waifus", "dir");
    os.makedirs(outdir + "/" + waifusdir, exist_ok=True);
    print("generating {}/{}/index.html from {}".format(outdir, waifusdir, waifussrc));
    copyfile(template, outdir + "/" + waifusdir + "/index.html");
    with open(waifussrc, "r") as contentfile:
        content = contentfile.read();
    replace(outdir + "/" + waifusdir + "/index.html", "{TITLE}", cfg.get("waifus", "title"));
    replace(outdir + "/" + waifusdir + "/index.html", "{INFO}", cfg.get("waifus", "header"));
    replace(outdir + "/" + waifusdir + "/index.html", "{CONTENT}", content);
    replace(outdir + "/" + waifusdir + "/index.html", "{TIME}", strftime("%d-%m-%Y", gmtime()));

def generateinteresting(special):
    if special:
        outdir = specialoutput;
    else:
       outdir = cfg.get("output", "dir");
    interestingsrc = cfg.get("interesting", "src");
    print("generating {}/interesting.html from {}".format(outdir, interestingsrc));
    copyfile(template, outdir + "/interesting.html");
    with open(interestingsrc, "r") as contentfile:
        content = contentfile.read();
    replace(outdir + "/interesting.html", "{TITLE}", cfg.get("interesting", "title"));
    replace(outdir + "/interesting.html", "{INFO}", cfg.get("interesting", "header"));
    replace(outdir + "/interesting.html", "{CONTENT}", content);
    replace(outdir + "/interesting.html", "{TIME}", strftime("%d-%m-%Y", gmtime()));

def generatelikes(special):
    if special:
        outdir = specialoutput;
    else:
       outdir = cfg.get("output", "dir");
    likesrc = cfg.get("like", "src");
    print("generating {}/like.html from {}".format(outdir, likesrc));
    copyfile(template, outdir + "/like.html");
    with open(likesrc, "r") as contentfile:
        content = contentfile.read();
    replace(outdir + "/like.html", "{TITLE}", cfg.get("like", "title"));
    replace(outdir + "/like.html", "{INFO}", cfg.get("like", "header"));
    replace(outdir + "/like.html", "{CONTENT}", content);
    replace(outdir + "/like.html", "{TIME}", strftime("%d-%m-%Y", gmtime()));


def generatedislikes(special):
    if special:
        outdir = specialoutput;
    else:
       outdir = cfg.get("output", "dir");
    dislikesrc = cfg.get("dislike", "src");
    print("generating {}/dislike.html from {}".format(outdir, dislikesrc));
    copyfile(template, outdir + "/dislike.html");
    with open(dislikesrc, "r") as contentfile:
        content = contentfile.read();
    replace(outdir + "/dislike.html", "{TITLE}", cfg.get("dislike", "title"));
    replace(outdir + "/dislike.html", "{INFO}", cfg.get("dislike", "header"));
    replace(outdir + "/dislike.html", "{CONTENT}", content);
    replace(outdir + "/dislike.html", "{TIME}", strftime("%d-%m-%Y", gmtime()));

if __name__ == "__main__":
    cfg = configparser.ConfigParser();
    cfg.read("settings.cfg");
    orgoutdir = cfg.get("output", "dir");
    if len(sys.argv) > 2:
        template = sys.argv[1];
        special = True; # if set output will be output/sys.argv[2]
        specialoutput = orgoutdir + "/" + sys.argv[2];
    else:
        special = False;
        template = cfg.get("output", "template");
    os.makedirs(orgoutdir, exist_ok=True);
    generateindex(special); # index
    generateblog(special); # blog with individual pages
    generateportfolio(special); # portfolio
    generateopinions(special); # opinions/anime
    generatewaifus(special); # my waifus
    generateinteresting(special); # interesting stuff
    generatelikes(special); # likes
    generatedislikes(special); #dislikes

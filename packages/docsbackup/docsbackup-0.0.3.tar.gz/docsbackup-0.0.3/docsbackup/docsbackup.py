#!/usr/bin/env python
# encoding: utf8
'''
Usage: googledownload [options] <url>...
       googledownload [options] -f <txt>
       googledownload [options] -y <sourcesyaml>
       googledownload [options] -x <docx>

  This script downloads the given google document.

Options:
    -d <dir>        directory to store output files
    -f <txt>        read from a text file
    -y <yaml>       yaml file with a list of urls
    -x <docx>       overview document with urls
    -o, --output=<yaml>
                    write out a dicitionary with url:filename mapping
    --errors=<yaml>
                    write list of failed urls to a yaml file
    -h, --help      show this help text
    -v, --verbose   show additional debug output
'''
from docopt import docopt
import os
import tempfile
import subprocess
from ruamel.yaml import YAML

from pprint import pformat
import logging
log = logging.getLogger()
logging.basicConfig(level=logging.INFO)
import shlex
import shutil
import re

import time

def export_url(url):
    '''
    fix a given document url and append corresponding export extension
    '''
    base, last = os.path.split(url)
    if last.startswith("edit") or last.startswith("export"):
        url=base
    if "docs.google.com/spreadsheets/" in base:
        url = os.path.join(base, "export?format=xlsx")
    elif "docs.google.com/document/" in base:
        url = os.path.join(base, "export?format=docx")
    elif "docs.google.com/presentation/" in base:
        url = os.path.join(base, "export/pptx")
    else:
        raise ValueError("unknown google docs format! can not export.")
    return url

def mangle_filename(oldname):
    '''
    add a timestamp version to the filename
    '''
    name, ext = os.path.splitext(oldname)
    assert not name.startswith("ServiceLogin"), "Need to be logged in to download this file"
    name = re.sub(r'.%80%93', "-", name) # remove part in broken filename
    name = name.replace("\udce2%80%99", " -")
    ext = re.match(r'(\.\w+).*', ext).group(1)  # remove "(invalid encoding)"
    return name + time.strftime("_%Y%m%d_%H%M") + ext

def fetch(url):
    '''
    fetch the given url and return filename of downloaded document
    '''
    curdir = os.getcwd()
    try:
        with tempfile.TemporaryDirectory() as tempdir:
            log.debug("tempdir %s", tempdir)
            os.chdir(tempdir)
            log.debug("wget --content-disposition %s", export_url(url))
            subprocess.check_call(shlex.split("wget --content-disposition '%s'" % export_url(url)))
            assert len(os.listdir()) == 1, "only one file must be downloaded!"
            oldname = os.listdir()[0]
            filename = mangle_filename(oldname)
            log.debug("move from '%s'", os.path.join(tempdir, oldname))
            log.debug("move to   '%s'", os.path.join(curdir, filename))
            shutil.move(os.path.join(tempdir, oldname), os.path.join(curdir, filename))
            return filename
    finally:
        os.chdir(curdir)

def load_docx(filename):
    '''
    extract google-doc urls from a word file using pandocs conversion to markdown

    Returns a list of strings.
    '''
    links = subprocess.check_output('pandoc -t markdown "%s" | egrep -o "http[s:/]+docs\.google\.com/[a-z]+/d/[-a-zA-Z0-9_]{33,44}/[a-z]+" | sort -u' % filename, shell=True)
    return links.decode("utf8").strip().split("\n")

def load_txt(filename):
    '''
    extract google-doc urls from a text file

    This function scans an inputfile using a regex and returns the list of
    strings of all matches. Duplicate entries are removed, document order is
    not preserved.
    '''
    import mmap
    links_re = re.compile(r"http[s:/]+docs\.google\.com/[a-z]+/d/[-a-zA-Z0-9_]{33,44}/[a-z]+")
    with open(filename, 'r+') as infile:
        #text = mmap.mmap(infile.fileno(), 0)
        text = infile.read()
        return list(set(links_re.findall(text)))

def main():
    args = docopt(__doc__)
    if args['--verbose']:
        log.setLevel(logging.DEBUG)
    log.debug(pformat(args))

    yaml = YAML(typ="safe")
    yaml.default_flow_style = True

    log.info("Hello World")
    urls = []
    if args["-y"]:
        with open(args["-y"], 'r') as infile:
            urls = yaml.load(infile)
        if isinstance(urls, dict):
            urls = urls.values()
    if args['-x']:
        urls.extend(load_docx(args['-x']))
    if args["<url>"]:
        urls.extend(args["<url>"])
    if args['-f']:
        urls.extend(load_txt(args['-f']))

    failed = []
    done = []
    linkmap = dict()
    for url in urls:
        try:
            log.info("fetching %s...", url)
            done.append(fetch(url))
            log.info("saved as %s", done[-1])
            linkmap[url] = done[-1]
        except AssertionError as e:
            log.error("downloading not successful: %s", e)
            failed.append(str(e)+ ": "+ url)
            linkmap[url] = "ERROR " + str(e)

    log.info("downloaded %d of %d documents", len(done), len(urls))
    assert len(done)+len(failed) == len(urls), "something is fishy"
    if failed:
        print("following documents could not be downloaded:")
        for name in failed:
            print(name)
        if args['--errors']:
            with open(args['--errors'], 'w') as outfile:
                yaml.dump(failed, stream=outfile)

    if args['--output']:
        log.info("saving index to %s", args['--output'])
        with open(args['--output'], 'w') as outfile:
            yaml.dump(linkmap, outfile)

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())

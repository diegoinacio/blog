# -*- coding: utf-8 -*-

'''
Copyright 2019 Diego Inácio

Author: Diego Inácio
GitHub: github.com/diegoinacio

Script to menage category and tag pages.
'''

import os
import re
import sys
import glob
import argparse
import colorama


parser = argparse.ArgumentParser()

parser.add_argument('--name', nargs='+')
parser.add_argument('--regex', default='.*', type=str)
parser.add_argument('--type', default='', type=str)
parser.add_argument('--show', action='store_true')
parser.add_argument('--create', action='store_true')
parser.add_argument('--remove', action='store_true')
parser.add_argument('--force', action='store_true')
parser.add_argument('--draft', action='store_true')

args = parser.parse_args()


colorama.init(autoreset=True)


PATH = os.path.abspath(os.path.curdir)
POSTSPATH = os.path.abspath(
    os.path.join(PATH, '..', '_posts')
)
CATSPATH = os.path.abspath(
    os.path.join(PATH, '..', 'category')
)
TAGSPATH = os.path.abspath(
    os.path.join(PATH, '..', 'tag')
)


# ! FEATURES and OPTIMIZATIONS
# TODO: split features into functions
# TODO: deal with types [categories and tags]
# TODO: implement regex filtering
# TODO: include drafts
# TODO: force creation of tracked cats and tags


def Show():
    CATS = glob.glob(os.path.join(CATSPATH, '*.html'))
    TAGS = glob.glob(os.path.join(TAGSPATH, '*.html'))
    POSTS = glob.glob(os.path.join(POSTSPATH, '*.html'))
    tCATS, uCATS, tTAGS, uTAGS = [], [], [], []
    # Scan tracked categories
    for CAT in CATS:
        cat = os.path.splitext(os.path.basename(CAT))[0]
        cat = ' '.join([e.capitalize() for e in cat.split('-')])
        tCATS += [cat]
    # Scan tracked tags
    for TAG in TAGS:
        tag = os.path.splitext(os.path.basename(TAG))[0]
        tag = ' '.join([e.capitalize() for e in tag.split('-')])
        tTAGS += [tag]
    # Scan untracked categories and tags
    for POST in POSTS:
        f = open(POST, 'r', encoding='utf8')
        fMatter = False
        for line in f:
            if line.strip() == '---':
                fMatter = not fMatter
            if fMatter:
                fmVar = line.strip().split()
                if fmVar[0] == 'categories:':
                    cats = line.replace('categories:', '').strip()[1:-1]
                    cats = [cat.strip() for cat in cats.split(',')]
                    cats = [cat for cat in cats if cat not in tCATS]
                    uCATS = list(set(cats + uCATS))
                if fmVar[0] == 'tags:':
                    tags = line.replace('tags:', '').strip()[1:-1]
                    tags = [tag.strip() for tag in tags.split(',')]
                    tags = [tag for tag in tags if tag not in tTAGS]
                    uTAGS = list(set(tags + uTAGS))
        f.close()
    # Sort tracked and untracked lists
    tCATS.sort()
    tTAGS.sort()
    uCATS.sort()
    uTAGS.sort()
    # Show categories and tags
    print('\n')
    print(
        colorama.Back.GREEN +
        colorama.Fore.BLACK +
        '.: Categories :.'
    )
    for CAT in tCATS:
        print(colorama.Fore.GREEN + CAT)
    for CAT in uCATS:
        print(colorama.Fore.RED + CAT)
    print('\n')
    print(
        colorama.Back.BLUE +
        colorama.Fore.BLACK +
        '.: Tags :.'
    )
    for TAG in tTAGS:
        print(colorama.Fore.GREEN + TAG)
    for TAG in uTAGS:
        print(colorama.Fore.RED + TAG)
    print('\n')


def Remove():
    CATS = glob.glob(os.path.join(CATSPATH, '*.html'))
    TAGS = glob.glob(os.path.join(TAGSPATH, '*.html'))
    for CAT in CATS:
        os.remove(CAT)
    for TAG in TAGS:
        os.remove(TAG)


def Create():
    CATS = glob.glob(os.path.join(CATSPATH, '*.html'))
    TAGS = glob.glob(os.path.join(TAGSPATH, '*.html'))
    POSTS = glob.glob(os.path.join(POSTSPATH, '*.html'))
    tCATS, uCATS, tTAGS, uTAGS = [], [], [], []
    # Scan tracked categories
    for CAT in CATS:
        cat = os.path.splitext(os.path.basename(CAT))[0]
        cat = ' '.join([e.capitalize() for e in cat.split('-')])
        tCATS += [cat]
    # Scan tracked tags
    for TAG in TAGS:
        tag = os.path.splitext(os.path.basename(TAG))[0]
        tag = ' '.join([e.capitalize() for e in tag.split('-')])
        tTAGS += [tag]
    # Scan untracked categories and tags
    for POST in POSTS:
        f = open(POST, 'r', encoding='utf8')
        fMatter = False
        for line in f:
            if line.strip() == '---':
                fMatter = not fMatter
            if fMatter:
                fmVar = line.strip().split()
                if fmVar[0] == 'categories:':
                    cats = line.replace('categories:', '').strip()[1:-1]
                    cats = [cat.strip() for cat in cats.split(',')]
                    cats = [cat for cat in cats if cat not in tCATS]
                    uCATS = list(set(cats + uCATS))
                if fmVar[0] == 'tags:':
                    tags = line.replace('tags:', '').strip()[1:-1]
                    tags = [tag.strip() for tag in tags.split(',')]
                    tags = [tag for tag in tags if tag not in tTAGS]
                    uTAGS = list(set(tags + uTAGS))
        f.close()
    # Create categories
    for CAT in uCATS:
        if CAT in tCATS:
            continue
        fMATTER = '---\n'
        fMATTER += 'layout:       category-page\n'
        fMATTER += 'title:        {}\n'.format(CAT)
        fMATTER += 'category:     {}\n'.format(CAT)
        fMATTER += 'menu_exclude: true\n'
        fMATTER += '---'
        filename = '-'.join([e.lower() for e in CAT.split()])
        filename = os.path.join(CATSPATH, filename + '.html')
        f = open(filename, 'w')
        f.write(fMATTER)
        f.close()
    for TAG in uTAGS:
        if TAG in tTAGS:
            continue
        fMATTER = '---\n'
        fMATTER += 'layout:       tag-page\n'
        fMATTER += 'title:        {}\n'.format(TAG)
        fMATTER += 'tag:          {}\n'.format(TAG)
        fMATTER += 'menu_exclude: true\n'
        fMATTER += '---'
        filename = '-'.join([e.lower() for e in TAG.split()])
        filename = os.path.join(TAGSPATH, filename + '.html')
        f = open(filename, 'w')
        f.write(fMATTER)
        f.close()


def Main():
    if args.show:
        Show()
    if args.remove:
        Remove()
    if args.create:
        Create()


if __name__ == '__main__':
	Main()
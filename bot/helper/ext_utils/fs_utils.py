from os import remove as osremove, path as ospath, mkdir, walk, listdir, rmdir
from sys import exit as sysexit
from json import loads as jsnloads
from shutil import rmtree
from PIL import Image
from magic import Magic
from subprocess import run as srun, check_output
from time import time
from math import ceil



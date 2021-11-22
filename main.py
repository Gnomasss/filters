import time

from slideShow import *
from filters import *
import os

dir = './img/'

ls = os.listdir(dir)

for i in range(len(ls)):
    getFilter(dir + ls[i])
    if i < len(ls) - 1:
        getTransform(dir + ls[i], dir + ls[i + 1])



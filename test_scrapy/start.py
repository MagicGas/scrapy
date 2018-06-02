import subprocess
import sys

param = sys.argv[1]
print(param)
ret = subprocess.getoutput("scrapy crawl %s --nolog"%param)
print(ret)
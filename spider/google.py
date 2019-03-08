import sys
from magic_google import MagicGoogle
import pprint
mg = MagicGoogle()
for i in mg.search(query=sys.argv[1], num=10):
    pprint.pprint(i)

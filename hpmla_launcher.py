import os, sys
import argparse


print('enter userscript')
parser = argparse.ArgumentParser()
parser.add_argument('--f', dest="f", required=True)
parser.add_argument('--glDir', dest="glDir", required=True)
parser.add_argument('--bd', dest="bd", required=True)
args = parser.parse_args()

print(args.f)
print(args.glDir)
print(args.bd)

code = os.system('/parasail/supersgd -l 1e-4 -k 32 -mc 1e-2 -e 10 -r 10 -f {0} -t 1 -gl 1 -glDir {1} -mem -bd {2}'.format(args.f, args.glDir, args.bd))
if code != 0:
    sys.exit(1)
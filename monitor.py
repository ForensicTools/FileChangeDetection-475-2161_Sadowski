#!/usr/bin/python
#Jackson Sadowski

from subprocess import Popen, PIPE

# Getting hashes of files
def getFileHashes(directory):

   (stdout, stderr) = Popen(["bash","/root/getFileHashes.sh"], stdout=PIPE).communicate()

   fileHashes = {}

   output = stdout.split('\n')

   for item in output:
      item = item.strip()
      if len(item) != 0:
         line = item.split()
         fileHashes[line[0]] = line[1]

   return fileHashes


# Main
def main():

   directory = "/root/check/"

   # Getting files
   fileHashes = getFileHashes(directory)

   print "=== File hashes ==="
   for k,v in fileHashes.items():
      print k, v

main()

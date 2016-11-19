#!/usr/bin/python
#Jackson Sadowski

from subprocess import Popen, PIPE
from time import sleep

# Getting hashes of files
def getFileHashes(directory):

   (stdout, stderr) = Popen(["bash","./getFileHashes.sh"], stdout=PIPE).communicate()

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

   directory = "./check/"

   # Getting files
   oldHashes = getFileHashes(directory)

   print "=== Initial File hashes ==="
   for k,v in oldHashes.items():
      print k, v
   print "==========================="
   print ""
   print "Monitoring directory.."
   print ""


   while True:
      newFileHashes = getFileHashes(directory)
      for k,v in newFileHashes.items():
         if k not in oldHashes.keys():
            print "File Updated: " + v
            print "Hash: " + k
            
      sleep(2)
      oldHashes = newFileHashes


main()


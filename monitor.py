#!/usr/bin/python
#Jackson Sadowski

import os
import sys
import json
import rethinkdb as r
import subprocess as sub
from subprocess import Popen, PIPE
from time import sleep

# Getting file stats
def getFileStats(fileName):
   
   fileStats = {}

   cmdarg = "--format=%n  %s  %b  %f  %u  %g  %D  %i  %h  %x  %y  %z  %w";

   (stdout, stderr) = sub.Popen(["stat", cmdarg, fileName], stdout=PIPE).communicate()

   stats = stdout.split('  ')


   fileStats['File'] = stats[0]
   fileStats['Size'] = stats[1]
   fileStats['Blocks'] = stats[2]
   fileStats['Hex Raw Mode'] = stats[3]
   fileStats['Owner UID'] = stats[4]
   fileStats['Group ID'] = stats[5]
   fileStats['Device Hex'] = stats[6]
   fileStats['INode Number'] = stats[7]
   fileStats['Hard Link count'] = stats[8]
   fileStats['Access'] = stats[9]
   fileStats['Modification'] = stats[10]
   fileStats['Status'] = stats[11]

   return fileStats


# Getting hashes of files
def getFileHashes(directory):

   (stdout, stderr) = sub.Popen(["bash","./getFileHashes.sh", directory], stdout=PIPE).communicate()

   fileHashes = {}

   output = stdout.split('\n')

   for item in output:
      item = item.strip()
      if len(item) != 0:
         line = item.split()
         fileHashes[line[1]] = line[0]

   return fileHashes


# Main
def main():
   directory = "/root/FileChangeDetection-475-2161_Sadowski/test"

   if len(sys.argv) == 2:
      directory = sys.argv[1]
   
   print "Monitoring: " + directory + "\n"

   conn = r.connect(host="jacksonsadowski.com", port=28015)

   # Getting files
   oldHashes = getFileHashes(directory)
   oldFileStats = {}
   
   # Putting init hashes into db
   print ""
   print "=== Initial File hashes ==="

   for fileName, shaHash in oldHashes.items():
      print fileName + " => " + shaHash
      oldFileStats[fileName] = getFileStats(fileName)
      r.db('file_log').table('sadowski').insert([{
         'event': 'initial', 'fileName': fileName, 
         'hash': shaHash, 'details': [oldFileStats[fileName]]
      }]).run(conn)

   print "==========================="
   print ""
   print "Monitoring directory.."
   print ""

   while True:

      # Rehashing directory
      newFileHashes = getFileHashes(directory)
      newFileStats = {} 
      # For all the items in the new hash
      for fileName, shaHash in newFileHashes.items():
         newFileStats[fileName] = getFileStats(fileName)
         
         # If the file hash changes
         if newFileHashes[fileName] != oldHashes[fileName]:

            r.db('file_log').table('sadowski').insert([{
               'event': 'hash_update', 'fileName': fileName,
               'hash': shaHash, 'details': [newFileStats[fileName]]  
            }]).run(conn)

            print "File Updated: " + fileName + " => " + shaHash
            oldHashes[fileName] = newFileHashes[fileName]

         # If the file stats changes
         if newFileStats[fileName] != oldFileStats[fileName]:

            r.db('file_log').table('sadowski').insert([{
               'event': 'stat_update', 'fileName': fileName,
               'hash': shaHash, 'details': [newFileStats[fileName]]  
            }]).run(conn)

            print "Stats Updated: " + fileName + " => " + shaHash 

            oldFileStats[fileName] = newFileStats[fileName]
            
            
      sleep(2)


main()


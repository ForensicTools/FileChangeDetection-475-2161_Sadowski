#File Change Detection

##Background
This project is for finding changes in a file system (or directory) and storing them into a RethinkDB instance.

##Technologies
- Bash / Python for detecting changes
- RethinkDB for Database

##Installing RethinkDB
For installing RethinkDB onto your local box, follow the instructions at https://www.rethinkdb.com/docs/install/

After installing, start the service using:
```service rethinkdb start```

##Downloading
```git clone https://github.com/ForensicTools/FileChangeDetection-475-2161_Sadowski.git```

##Usage
```./monitor.py [directory]```

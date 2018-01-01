# BugState
This scrips will go over _meaningful_ bugs that were opened in each
major RHOSP version starting in Newton. The output of it is a simple csv
that can be used, for instance to calculate changes between versions for
a specific group.
## Notice
This tool uses custom fields specific for Red Hat and as such requires
that you have a user with sufficient permissions for it to work.
## Usage
This script was written with python 2.7 in mind, so make sure that you have
that and the latest version of python-bugzilla:
```
 # _your favorite pkg manager_ update/upgrade
 # pip install python-bugzilla
```
Once installed, run this command once to create a working token:
```
 > bugzilla --login
Logging into bugzilla.redhat.com
Bugzilla Username: nosuchuser@redhat.com
Bugzilla Password:
```
You might see this error: Unexpected action 'None' if a token file was
created in  ~/.cache/python-bugzilla/ then you should be fine.

Now you can 'git clone' this to anywhere and run the script via python:
```
 > python path-to-clone/bugstate.py
```
### TODO
Is written in a file called TODO.

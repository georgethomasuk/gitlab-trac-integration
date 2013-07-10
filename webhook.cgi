#!/usr/bin/env python

import cgi
import os
import json
import sys
from urlparse import parse_qs
from operator import itemgetter
from subprocess import call

#Enables debug output when modifying
#import cgitb
#cgitb.enable()

#The path to your trac projects folder
TRAC_ENV = '/var/trac/projects/'


def process_commits():
    """
    Takes details of commits sent by a post-receive call from GitLab
    and fires calls to close and reference tickets in Trac.

    The project_name should be provided in the query string:
        ?project_name=myproject

    GitLab will then send the commit data as JSON in the request body
    """

    #Get the project name from the query string
    query_string = parse_qs(os.environ['QUERY_STRING'])
    if not 'project_name' in query_string:
        return

    if len(query_string['project_name']) == 0:
        #If no project_name provided then assume '(default)'
        project_name = '(default)'
    elif len(query_string['project_name']) > 1:
        #If multiple projects names passed then exit
        return
    else:
        #Assign the project name
        project_name = query_string['project_name'][0]

    #Load the commit details from the request body
    json_data = json.load(sys.stdin)

    #Get the repo name form the query string (first) then json
    if not 'repo_name' in query_string:
        repo_name = json_data['repository']['name']
    else:
        if len(query_string['repo_name']) == 0:
            #If no respo_name provided then exit
            repo_name = json_data['repository']['name']
        elif len(query_string['repo_name']) > 1:
            #If multiple repos names passed then exit
            return
        else:
            #Assign the repo name
            repo_name = query_string['repo_name'][0]

    #Get a list of the new commits
    pending_commits = map(itemgetter('id'), json_data['commits'])

    #Make a call for each Trac commit
    #TODO: Is probably possible to do in one call
    for commit in pending_commits:
        command = ["trac-admin", "%s%s" % (TRAC_ENV, project_name), "changeset", "added", "'%s'" % repo_name, "%s" % commit]
        print command
        call(command)

#Return an empty reponse
print "Content-type:text/html\r\n\r\n"
print ''

#Call the function to process the commits
process_commits()

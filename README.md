gitlab-trac-integration
=======================

Provide a Trac webhook for GitLab to call and update ticket information.

The end goal is to make this a Trac plugin. However for now this is a cgi script to be run by your webserver of choice

GitLab Webhook Configuration
----------------------------

Your GitLab webhook should be pointed at:

    http://127.0.0.1/pathtohook?project_name=<tracprojectname>

If no Trac project name is specified in the query string, then it will use the default project.


Apache Configuration
--------------------
Be carefult when exposing this webhook, as it may expose your system or Trac repositories in undesirable ways.

    ScriptAlias /hooks/ "/var/trac/cgi-bin/gitlab-trac-integration"

    <Directory "/var/trac/cgi-bin/gitlab-trac-integration">
        AllowOverride None
        Options None
        Order allow,deny
        Allow from all
    </Directory>

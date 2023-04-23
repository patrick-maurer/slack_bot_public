This Slack application enables users to conveniently check the status of APS articles. Once installed within a local workspace, the application communicates with users via direct message.

The application accepts four distinct commands: /add code name, /get_status, /del code, and /reset. The 'code' and 'name' parameters used in these commands correspond to the data required by the APS website. Upon execution of the '/add' command, the specified article is added to a designated database.

In order to access the database and Slack API, users must provide the necessary environmental variables. 

All required packages can be installed via the 'requirements.txt' file.
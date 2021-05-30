## **Practical Task 2**
####The script is a websocket-server that responds to the request response with the celestial coordinates of the moon every 10 seconds.

###How does he work
####to start the server, you need to call main.py from the command line, the server starts and automatically starts ngrok, which makes the local host public, it follows that for the script to work before starting, you need to install ngrok in your OS and log in / register (to do this, go to http: // ngrok.com/).
####the server's work is based on the websockets package, the server works using asynchronous functions, from which it follows that the server will work relatively quickly
###a little about calculations
####in the calculations of the coordinates of the moon there are some inaccuracies since, as you know, the trajectory of rotation around the earth is elliptical, for convenience of calculations I assumed that the trajectory of rotation of the line is circular, which in turn causes a few deviations.
###and lastly
####this is vol. 1 of the script if there are any comments I will be happy to correct
### Building and Running
------------------------
1. ```cd to siege_loadtest/```
2. ```docker build -t jcostello84/siege_loadtest .```

NOTE: You do not need to build locally in order to run this app. 

To run, pass your custom parameters using the following format:

```docker run -it -e DOMAIN="http://www.example.com" -e LOGIN_URL="/login.php&username=siegeuser%40someplace.com&password=Pa55word" -e USERNAME="siegeuser%40someplace.com" -e PASSWORD="Pa55word" -e URL_LIST="/userHome.php?page=accounting|/get.php|/api/JsonRPC/add_image/ POST /opt/post_json/post_image.json|/search?q=searchterm" jcostello84/siege_loadtest -v -c5 -r5```

1. ```DOMAIN=https://www.<SET_BASE_URL>.com``` Make sure to set http or https depending on your sites setup.
2. ```LOGIN_URL="/login.php?username=siegeuser%40someplace.com&password=Password1&remember=1&softLogin=false"```
3. ```URL_LIST="/userHome.php?page=accounting|/get.php|/api/JsonRPC/add_image/ POST /opt/post_json/post_image.json"```
4. ```USERNAME="siegeuser%40someplace.com"```
5. ```PASSWORD="Password1" ```
6. ```ETC_HOSTS="192.168.1.1 www.example.com admin.example.com assets.example.com"```

### Supported Commands
------------------------
For more detailed documentation please see the [Siege Docs](http://linux.die.net/man/1/siege). Siege supports the following command line options:

###### -V, --version
VERSION, prints the version number

###### -h, --help
HELP, prints the help section which includes a summary of all the command line options.

###### -C, --config
CONFIGURATION, prints the current configuration in the $HOME/.siegerc file. Edit that file to set flag values for EVERY siege run, a feature which eases runtime invocation. You set an alternative resource file with the SIEGERC environment variable: export SIEGERC=/home/jeff/haha

###### -v, --verbose
VERBOSE, prints the HTTP return status and the GET request to the screen. Useful when reading a series of URLs from a configuration file. This flag allows you to witness the progress of the test.

###### -q, --quiet
QUIET turns off verbose and suppresses most output. This option was added primarily for scripting with -g/--get. If you run a full siege in quiet mode, you'll still get the opening introduction and the final stats.

###### -g, --get
GET HTTP headers and display the transaction. Siege exits 1 if the transaction doesn't contain at least one HTTP 200 response, otherwise it exits 0. You can limit the transaction to just the headers by setting gmethod=HEAD in $HOME/.siegerc

###### -c NUM, --concurrent=NUM
CONCURRENT, allows you to set the concurrent number of simulated users to num. The number of simulated users is limited to the resources on the computer running siege.

###### -i, --internet
INTERNET, generates user simulation by randomly hitting the URLs read from the urls.txt file. This option is viable only with the urls.txt file.

###### -d NUM, --delay=NUM
DELAY, each siege simulated users sleeps for a random interval in seconds between 0 and NUM.

###### -b, --benchmark
BENCHMARK, runs the test with NO DELAY for throughput benchmarking. By default each simulated user is invoked with at least a one second delay. This option removes that delay. It is not recommended that you use this option while load testing.

###### -r NUM, --reps=NUM, --reps=once
REPS, allows you to run the siege for NUM repetitions. If --reps=once, then siege will run through the urls.txt file one time and stop when it reaches the end. NOTE: -t/--time takes precedent over -r/--reps. If you want to use this option, make sure time = x is commented out in your $HOME/.siegerc file.

###### -t NUMm, --time=NUMm
TIME, allows you to run the test for a selected period of time. The format is "NUMm", where NUM is a time unit and the "m" modifier is either S, M, or H for seconds, minutes and hours. To run siege for an hour, you could select any one of the following combinations: -t3600S, -t60M, -t1H. The modifier is not case sensitive, but it does require no space between the number and itself.

###### -l [FILE], --log[=FILE]
LOG transaction stats to FILE. The argument is optional. If FILE is not specified, then siege logs the transaction to SIEGE_HOME/var/siege.log. If siege is installed in /usr/local, then the default siege.log is /usr/local/var/siege.log. This option logs the final statistics reported when siege successfully completes its test. You can edit $HOME/.siegerc to change the location of the siege.log file.

###### -m MESSAGE, --mark=MESSAGE
MARK, mark the log file with a separator. This option will allow you to separate your log file entries with header information. This is especially useful when testing two different servers. It is not necessary to use both the -m option and the -l option. -m assumes -l so it marks and logs the transaction. If the MESSAGE has spaces in it, make sure that you put it in quotes.

###### -H HEADER, --header=HEADER
HEADER, this option allows you to add additional header information.

###### -R SIEGERC, --rc=SIEGERC
RC, sets the siegerc file for the run. This option overrides the environment variable SIEGERC and the default resource file, $HOME/.siegerc

###### -f FILE, --file=FILE
FILE, the default URL file is SIEGE_HOME/etc/urls.txt. To select a different URL file, use this option, i.e., siege -f myurls.txt

###### -A "User Agent", --user-agent="User Agent"
AGENT, use this option to set the User-Agent in the request.

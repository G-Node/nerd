##How-To setup enviroment for orientdb application
___

####[OrientDB] installation:
* Download latest version from project site: [orientdb-graphed-1.0.1]
* Unzip files, go to the **/bin** directory
* Run orientdb server

        sh server.sh

* Run orient console in order to create new database

        sh console.sh
        
*   Create nerd database (change path for your system)

        create database local:/home/mokrzu/Downloads/orientdb-graphed-1.0.1/databases/nerd_db admin admin local graph

####[Rexster] server installation:
It's intermediate layer between python driver and orientDB instance.

*   Download and run rexster installation:

        git clone https://github.com/tinkerpop/rexster.git
        cd rexster
        mvn clean install

* Enable orientdb connection in configuration file: **/rexster/rexster-server/rexster.xml**
    
        <graph>
            <graph-name>nerd_db</graph-name>
            <graph-type>orientgraph</graph-type>
            <graph-location>local:/home/mokrzu/Downloads/orientdb-graphed-1.0.1/databases/nerd_db</graph-location>
            <extensions>...</extensions>
            <properties>
                <username>admin</username>
                <password>admin</password>
            </properties>
        </graph>

* Disable gratfulgraph sample becouse it causes some errors:

            <graph>
                <graph-enabled>false</graph-enabled>
                <graph-name>gratefulgraph</graph-name>

* Now, run it:

        sh /rexster/rexster-server/rexster.sh --start

* If configuration was done properly, in console logs you should see:

        [INFO] RexsterApplicationGraph - Graph [nerd_db] - configured with allowable namespace [tp:gremlin]
        [INFO] GraphConfigurationContainer - Graph nerd_db - orientgraph[local:/home/mokrzu/Downloads/orientdb-graphed-1.0.1/databases/nerd_db] loaded

* There is also available web based GUI for Rexster at: http://localhost:8182/doghouse/
Works fine under Chrome browser.
[orientdb-graphed-1.0.1]: http://code.google.com/p/orient/downloads/detail?name=orientdb-graphed-1.0.1.zip&can=2&q=
[Rexster]:
https://github.com/tinkerpop/rexster/wiki/
[OrientDB]:
http://www.orientdb.org/orient-db.htm
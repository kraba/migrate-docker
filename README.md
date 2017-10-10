# migrate-docker , a python script to import db dump in a Docker container

### Version

0.1-dev

### Why?

It's simple...I want to learn [Docker SDK](https://docker-py.readthedocs.io/en/stable/) and improve/learn my Python knownledge.

### Description

Edit and modify ```conf.json``` with the required data:
1. DBDumpFile = the dump file (local and with .sql extension) of your old DB
2. DBUser = user of your DB in Docker container
3. DBPass = the password of DBUser in Docker container
4. DBName = the name of DB to import in Docker container
5. DBDocker = the name of Docker Container

and launch it:
```
./mygrate.py
```

### Requirements

Docker...of course...and two python package: magic & docker
```
pip install docker
pip install magic
```

### Author

Matteo Basso - matteo (dot) basso (at) gmail (dot) com

### License

This software is licensed under GPL v3 license.

Copyright (c) 2017 Matteo Basso

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You can read the full text of the GNU General Public License version 3
[here](http://www.gnu.org/licenses/).


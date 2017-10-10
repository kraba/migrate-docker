#!/usr/bin/python
"""Docker utility to migrate db dump or files to a docker container.

Read: conf.json file. Yes..it's a simple and bugged script.
Author Matteo Basso - matteo (dot) basso (at) gmail (dot) com
Date: 20171009
Version: 0.1
To do: exception + images + other cases

License:
    mygrate.py is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    mygrate/migrate-docker is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with mygrate.py. If not, see <http://www.gnu.org/licenses/>.
"""

import json
import magic
import docker
import tarfile


def jsonToDict():
    """Copy json key+value to a dict."""
    with open('conf.json') as data_file:
        data = json.load(data_file)
    return data


def checkJson(data):
    """Verify all value of json config file.

    If a value is not present ask to insert it.
    """
    for key, section in data.items():
        for attribute, value in section.items():
            if not value:
                section[attribute] = raw_input('Value of \"{}\" is not '
                                               'present, please insert it: '
                                               .format(attribute))
    return data


def printJson(data):
    """Print the dict and ask if it's correct."""
    for key, section in data.items():
        print key
        for attribute, value in section.items():
            print('{} : {}'.format(attribute, value))
    return raw_input('Type Y/y if all values are correct or N/n if you: ')


def containerIsRun(key, value):
    """Getting info of Container.

    Container exists? Running or Exited. Otherwise doesen't exists.
    TODO: docker.errors.NotFound: 404 Client Error: Not Found
        ("No such container: nomedocker")
    """
    container = clientDocker.containers.get(data[key][value])
    if container.status != "running":
        print('Argh! Container {} is not running! Do you want to start it?'
              .format(container.name))
        if raw_input('Type Y/y to start it, any other keys to exit: ') \
           not in ('y', 'Y'):
            print('Check container name and relaunch!')
            exit()
        else:
            print('Container {} is starting'.format(container.name))
            container.start()
            print('... {} is {}'
                  .format(container.name,
                          clientDocker.containers.get(data[key]
                                                      [value]).status))
            return
    print('Container {} is running...'.format(container.name))


def recoverMime(filetype):
    """Extract the mime type of request value."""
    return (magic.from_file(filetype, mime=True).split("/")[1:])[0]


def importSql(key, value):
    """Import the DB Dump."""
    dbName = data[key]['DBName']
    dbUser = data[key]['DBUser']
    dbPass = data[key]['DBPass']
    dbFile = data[key]['DBDumpFile']
    dbDocker = data[key][value]
    container = clientDocker.containers.get(data[key][value])
    """Query to check if DB exists"""
    dbExists = ("mysql -u {} -p{} -s -e \"SHOW DATABASES LIKE '{}'\""
                .format(dbUser, dbPass, dbName))
    """If doesn't exists...check user to create it """
    if container.exec_run(dbExists, stderr=False).rstrip() != dbName:
        print('Argh! DB {} doesn\'t exists! Do you want to create it?'
              .format(dbName))
        if raw_input('Type Y/y to create it, any other keys to exit: ') \
           not in ('y', 'Y'):
            print('Check DB name and relaunch!')
            exit()
        else:
            print('DB {} - {} container is on creation'.format(
                dbName, data[key]['DBDocker']))
            dbCreation = ('mysql -u {} -p{} -s -e \"CREATE DATABASE {};\"'
                          .format(dbUser, dbPass, dbName))
            container.exec_run(dbCreation, stderr=False)
            return importSql('database', 'DBDocker')
    else:
        with tarfile.open("dbdump.tar", "w") as tarSql:
            tarSql.add(dbFile)
        with open("dbdump.tar", "rb") as extractDump:
            container.put_archive('/tmp/', extractDump)
        fileSql = ('/tmp/{}'.format(dbFile))
        importDump = ('mysql -u {} -p{} -s -e \"use {}; source {}\"'
                      .format(dbUser, dbPass, dbName, fileSql))
        container.exec_run(importDump, stderr=False)
        print('DB {} imported on {} container'.format(dbName, dbDocker))


correctCycle = 'n'
print('Checking json config file\n')
while correctCycle not in ('y', 'Y'):
    data = jsonToDict()
    correctCycle = printJson(checkJson(data))

"""Initialize clientDocker."""
clientDocker = docker.from_env()

"""Check DB Docker"""
containerIsRun('database', 'DBDocker')

"""Check File MIME
TODO: uncompress/check file compressed
#if recoverMime(data["database"]["DBDumpFile"]) != "plain":
#    print('File {} is not an .sql plain text, please check/uncompress it'
#          '\nScript will die/exit!!!'.format(data["database"]["DBDumpFile"]))
#    exit()
"""

"""Execute import DB"""
importSql('database', 'DBDocker')

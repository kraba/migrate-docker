#!/usr/bin/python
"""Docker utility to migrate db dump or files to a docker container."""

import json
import magic
import docker


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
    TODO: gestire docker.errors.NotFound: 404 Client Error: Not Found
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


"""
def importSql(data):
    mime = recoverMime(data["database"]["dump"])
    if mime != "plain":
        pass
    else:
        if not data["database"]["dbpass"]:
            pass
"""

correctCycle = 'n'
print('Checking json config file\n')
while correctCycle not in ('y', 'Y'):
    data = jsonToDict()
    correctCycle = printJson(checkJson(data))

"""Initialize clientDocker."""
clientDocker = docker.from_env()
"""Check DB Docker"""
containerIsRun('database', 'DockerDB')
print "nemo vanti"

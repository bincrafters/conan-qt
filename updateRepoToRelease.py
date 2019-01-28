#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import json
import shutil
import urllib.request
import urllib.error


def getsubmodules():
    import configparser
    config = configparser.ConfigParser()
    config.read('qt/qtmodules.conf')
    res = {}
    assert config.sections()
    for s in config.sections():
        section = str(s)
        assert section.startswith("submodule ")
        assert section.count('"') == 2
        modulename = section[section.find('"') + 1: section.rfind('"')]
        status = str(config.get(section, "status"))
        if status != "obsolete" and status != "ignore":
            res[modulename] = {"branch": str(config.get(section, "branch")), "status": status,
                               "path": str(config.get(section, "path")), "depends": []}
            if config.has_option(section, "depends"):
                res[modulename]["depends"] = [str(i) for i in config.get(section, "depends").split()]
    return res


def downloadconfig(module, path, version):
    configpath = 'qt/' + module + path
    os.makedirs(configpath)
    try:
        urllib.request.urlretrieve(
            'http://code.qt.io/cgit/qt/' + module + '.git/plain' + path + '/config_help.txt?h=v' + version,
            os.path.join(configpath, 'config_help.txt')
        )
    except urllib.error.HTTPError:
        pass
    configfile = configpath + '/configure.json'
    try:
        urllib.request.urlretrieve(
            'http://code.qt.io/cgit/qt/' + module + '.git/plain' + path + '/configure.json?h=v' + version,
            configfile
        )
    except urllib.error.HTTPError:
        print('skipping module ' + module)
        return

    with open(configfile) as json_data:
        d = json.load(json_data, strict=False)
    if 'subconfigs' in d:
        for subconfig in d['subconfigs']:
            downloadconfig(module, path + '/' + subconfig, version)


def downloadfiles(version):
    urllib.request.urlretrieve('http://code.qt.io/cgit/qt/qt5.git/plain/.gitmodules?h=v' + version, 'qt/qtmodules.conf')
    for mod in getsubmodules():
        downloadconfig(mod, "", version)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please use only one parameter: the Qt version written x.y.z")
        sys.exit(2)

    shutil.rmtree('qt')
    os.mkdir('qt')
    downloadfiles(sys.argv[1])

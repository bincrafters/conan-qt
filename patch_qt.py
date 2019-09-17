#!/usr/bin/env python
#############################################################################
##
## Copyright (C) 2019 The Qt Company Ltd.
## Contact: https://www.qt.io/licensing/
##
## This file is part of the release tools of the Qt Toolkit.
##
## $QT_BEGIN_LICENSE:GPL-EXCEPT$
## Commercial License Usage
## Licensees holding valid commercial Qt licenses may use this file in
## accordance with the commercial license agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and The Qt Company. For licensing terms
## and conditions see https://www.qt.io/terms-conditions. For further
## information use the contact form at https://www.qt.io/contact-us.
##
## GNU General Public License Usage
## Alternatively, this file may be used under the terms of the GNU
## General Public License version 3 as published by the Free Software
## Foundation with exceptions as appearing in the file LICENSE.GPL3-EXCEPT
## included in the packaging of this file. Please review the following
## information to ensure the GNU General Public License requirements will
## be met: https://www.gnu.org/licenses/gpl-3.0.html.
##
## $QT_END_LICENSE$
##
#############################################################################

import os
import re
import fileinput


def _fileIterator(artifactsDir):
    print('Patching build time paths from: {0}'.format(artifactsDir))
    for root, dirs, files in os.walk(artifactsDir):
        for fileName in files:
            yield os.path.join(os.path.join(root, fileName))


def _getPatchers(product):
    if product == 'qt_framework':
        return [patchAbsoluteLibPathsFromFile, eraseQmakePrlBuildDir, patchQConfigPri]
    else:
        # default
        return [patchAbsoluteLibPathsFromFile, eraseQmakePrlBuildDir]


def patchFiles(artifactsDir, product):
    print('Patching files from: {0}'.format(artifactsDir))
    patchers = _getPatchers(product)
    for filePath in _fileIterator(artifactsDir):
        for patcher in patchers:
            patcher(filePath)


def patchQtEdition(artifactsDir, licheckFileName, releaseDate):
    for root, dirs, files in os.walk(artifactsDir):
        for fileName in files:
            if fileName == 'qconfig.pri':
                _patchQtEdition(os.path.join(root, fileName), licheckFileName, releaseDate)
                return


def _patchQtEdition(filePath, licheckFileName, releaseDate):
    for line in fileinput.FileInput(filePath, inplace=True):
        if 'QT_EDITION' in line:
            edition_line = 'QT_EDITION = Enterprise'
            licheck_line = 'QT_LICHECK = ' + licheckFileName
            release_line = 'QT_RELEASE_DATE = ' + releaseDate
            print(edition_line.rstrip('\n'))
            print(licheck_line.rstrip('\n'))
            print(release_line.rstrip('\n'))
        else:
            print(line.rstrip('\n'))


def patchQConfigPri(filePath):
    for line in fileinput.FileInput(filePath, inplace=True):
        patchedLine = patchQConfigPriFromLine(line)
        print(patchedLine.rstrip('\n'))


def patchQConfigPriFromLine(line):
    if 'QMAKE_DEFAULT_LIBDIRS' in line:
        return line.split('=')[0].strip() + ' ='
    if 'QMAKE_DEFAULT_INCDIRS' in line:
        return line.split('=')[0].strip() + ' ='
    else:
        return line


def eraseQmakePrlBuildDir(filePath):
    # Erase lines starting with 'QMAKE_PRL_BUILD_DIR' from .prl files
    for line in fileinput.FileInput(filePath, inplace=True):
        patchedLine = patchQmakePrlBuildDirFromLine(line)
        print(patchedLine.rstrip('\n'))


def patchQmakePrlBuildDirFromLine(line):
    return '' if line.startswith('QMAKE_PRL_BUILD_DIR') else line


def patchAbsoluteLibPathsFromFile(filePath):
    for line in fileinput.FileInput(filePath, inplace=True):
        patchedLine = patchAbsoluteLibPathsFromLine(line, filePath.split(".")[-1])
        print(patchedLine.rstrip('\n'))


def patchAbsoluteLibPathsFromLine(line, fileExtension):
    """
    Captures XXX in e.g. /usr/lib/libXXX.so, /usr/lib64/libXXX.a, and C:\XXX.lib
    Paths are not allowed to contain whitespace though
      [^\s\"]+ - start of path
      "/lib", [\\/]
      ([a-zA-Z0-9\_\-\.\+]+) - capture group for the actual library name
      ".so", ".a", ".lib" suffix
      (\.[0-9]+)? - capture group for for versioned libraries
    """

    def _removeWhiteSpace(line):
        """Remove white space from paths if found inside quoted blocks."""
        eraseEnabled = False
        result = ""
        for char in line:
            if char == "\"":
                # toggle on/off
                eraseEnabled = not eraseEnabled
            if eraseEnabled and char == " ":
                continue
            result += char
        return result

    if fileExtension == "cmake":
        # from cmake files patch only lines containing "find_extra_libs"
        cmakeFindExtraLibsSearchRegexp = re.compile(r'_*._find_extra_libs\(')
        if not re.search(cmakeFindExtraLibsSearchRegexp, line):
            return line

    expressions = [
        re.compile(r'[^\s\"]+/lib([a-zA-Z0-9\_\-\.\+]+)\.(so|a|tbd)(\.[0-9]+)?\b'),
        re.compile(r'[^\s\"]+[\\/]([a-zA-Z0-9\_\-\.\+]+)\.(lib)(\.[0-9]+)?\b')
    ]

    def _substituteLib(match):
        if (match.group(0).startswith("$$[QT_")):
            return match.group(0)
        result = "" if fileExtension == "cmake" else "-l"  # .pri, .prl, .la, .pc
        result += match.group(1)
        return result

    for regex in expressions:
        # check if there are any matches?
        if re.search(regex, line):
            line = _removeWhiteSpace(line)
            line = regex.sub(_substituteLib, line)
            break

    return line
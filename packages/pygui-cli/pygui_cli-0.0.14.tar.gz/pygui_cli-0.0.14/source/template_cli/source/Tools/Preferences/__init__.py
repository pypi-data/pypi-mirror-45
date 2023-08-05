# -*- coding: utf-8 -*-

# Copyright (c) 2002 - 2017 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Package implementing the preferences interface.

The preferences interface consists of a class, which defines the default
values for all configuration items and stores the actual values. These
values are read and written to the eric6 preferences file by module
functions. The data is stored in a file in a subdirectory of the users home
directory. The individual configuration data is accessed by accessor functions
defined on the module level. The module is simply imported wherever it is
needed with the statement 'import Preferences'. Do not use
'from Preferences import *' to import it.
"""

from __future__ import unicode_literals

from PyQt5.QtCore import QSettings

from ..Globals import *

try:
    basestring  # __IGNORE_WARNING__
except NameError:
    basestring = str

import os
import fnmatch
import shutil
import json
import sys


class Prefs(object):
    settings = None
    """
    A class to hold all configuration items for the application.
    一个类，用于保存应用程序的所有配置项。
    """
    # defaults for the variables window
    varDefaults = {
        "LocalsFilter": "[]",
        "GlobalsFilter": "[]"
    }


    # defaults for Code Documentation Viewer
    docuViewerDefaults = {
        "ShowInfoAsRichText": False,
        "Provider": "disabled",
        "ShowInfoOnOpenParenthesis": True,
    }


def initRecentSettings():
    """
    Module function to initialize the central configuration store for recently
    opened files and projects.
    用于初始化最近的中央配置存储打开文件和项目。
    This function is called once upon import of the module.
    此函数在模块导入时调用一次
    """
    Prefs.rsettings = QSettings(
        QSettings.IniFormat, QSettings.UserScope,
        settingsNameOrganization, settingsNameRecent)
def initPreferences():
    """
    Module function to initialize the central configuration store.
    初始化配置
    """
    Prefs.settings = QSettings(
        QSettings.IniFormat, QSettings.UserScope,
        settingsNameOrganization, settingsNameGlobal)
    if not isWindowsPlatform():
        hp = QDir.homePath()
        dn = QDir(hp)
        dn.mkdir(".eric6")
    QCoreApplication.setOrganizationName(settingsNameOrganization)
    QCoreApplication.setApplicationName(settingsNameGlobal)

    # Avoid nasty behavior of QSettings in combination with Py2
    Prefs.settings.value("UI/SingleApplicationMode")


initPreferences()
initRecentSettings()

# -------------future may be used------------- ↓

# def readToolGroups(prefClass=Prefs):
#     """
#     Module function to read the tool groups configuration.
#
#     @param prefClass preferences class used as the storage area
#     @return list of tuples defing the tool groups
#     """
#     toolGroups = []
#     groups = int(prefClass.settings.value("Toolgroups/Groups", 0))
#     for groupIndex in range(groups):
#         groupName = prefClass.settings.value(
#             "Toolgroups/{0:02d}/Name".format(groupIndex))
#         group = [groupName, []]
#         items = int(prefClass.settings.value(
#             "Toolgroups/{0:02d}/Items".format(groupIndex), 0))
#         for ind in range(items):
#             menutext = prefClass.settings.value(
#                 "Toolgroups/{0:02d}/{1:02d}/Menutext".format(groupIndex, ind))
#             icon = prefClass.settings.value(
#                 "Toolgroups/{0:02d}/{1:02d}/Icon".format(groupIndex, ind))
#             executable = prefClass.settings.value(
#                 "Toolgroups/{0:02d}/{1:02d}/Executable".format(
#                     groupIndex, ind))
#             arguments = prefClass.settings.value(
#                 "Toolgroups/{0:02d}/{1:02d}/Arguments".format(groupIndex, ind))
#             redirect = prefClass.settings.value(
#                 "Toolgroups/{0:02d}/{1:02d}/Redirect".format(groupIndex, ind))
#
#             if menutext:
#                 if menutext == '--':
#                     tool = {
#                         'menutext': '--',
#                         'icon': '',
#                         'executable': '',
#                         'arguments': '',
#                         'redirect': 'no',
#                     }
#                     group[1].append(tool)
#                 elif executable:
#                     tool = {
#                         'menutext': menutext,
#                         'icon': icon,
#                         'executable': executable,
#                         'arguments': arguments,
#                         'redirect': redirect,
#                     }
#                     group[1].append(tool)
#         toolGroups.append(group)
#     currentGroup = int(
#         prefClass.settings.value("Toolgroups/Current Group", -1))
#     return toolGroups, currentGroup
#
#
# def syncPreferences(prefClass=Prefs):
#     """
#     Module function to sync the preferences to disk.
#
#     In addition to syncing, the central configuration store is reinitialized
#     as well.
#
#     @param prefClass preferences class used as the storage area
#     """
#     prefClass.settings.setValue("General/Configured", True)
#     prefClass.settings.sync()
#
#
# def exportPreferences(prefClass=Prefs):
#     """
#     Module function to export the current preferences.
#     导出首选项
#     @param prefClass preferences class used as the storage area
#     """
#     filename, selectedFilter = E5FileDialog.getSaveFileNameAndFilter(
#         None,
#         QCoreApplication.translate("Preferences", "Export Preferences"),
#         "",
#         QCoreApplication.translate(
#             "Preferences",
#             "Properties File (*.ini);;All Files (*)"),
#         None,
#         E5FileDialog.Options(E5FileDialog.DontConfirmOverwrite))
#     if filename:
#         ext = QFileInfo(filename).suffix()
#         if not ext:
#             ex = selectedFilter.split("(*")[1].split(")")[0]
#             if ex:
#                 filename += ex
#         settingsFile = prefClass.settings.fileName()
#         prefClass.settings = None
#         shutil.copy(settingsFile, filename)
#         initPreferences()
#
#
# def importPreferences(prefClass=Prefs):
#     """
#     Module function to import preferences from a file previously saved by
#     the export function.
#     导入首选项
#     @param prefClass preferences class used as the storage area
#     """
#     filename = E5FileDialog.getOpenFileName(
#         None,
#         QCoreApplication.translate("Preferences", "Import Preferences"),
#         "",
#         QCoreApplication.translate(
#             "Preferences",
#             "Properties File (*.ini);;All Files (*)"))
#     if filename:
#         settingsFile = prefClass.settings.fileName()
#         shutil.copy(filename, settingsFile)
#         initPreferences()
#
#
# def isConfigured(prefClass=Prefs):
#     """
#     Module function to check, if the the application has been configured.
#
#     @param prefClass preferences class used as the storage area
#     @return flag indicating the configured status (boolean)
#     """
#     return toBool(prefClass.settings.value("General/Configured", False))
#
#
#
#
# def getVarFilters(prefClass=Prefs):
#     """
#     Module function to retrieve the variables filter settings.
#
#     @param prefClass preferences class used as the storage area
#     @return a tuple defining the variables filter
#     """
#     localsFilter = eval(prefClass.settings.value(
#         "Variables/LocalsFilter", prefClass.varDefaults["LocalsFilter"]))
#     globalsFilter = eval(prefClass.settings.value(
#         "Variables/GlobalsFilter", prefClass.varDefaults["GlobalsFilter"]))
#     return (localsFilter, globalsFilter)
#
#
# def getSystem(key, prefClass=Prefs):
#     """
#     Module function to retrieve the various system settings.
#
#     @param key the key of the value to get
#     @param prefClass preferences class used as the storage area
#     @return the requested system setting
#     """
#     from Utilities import supportedCodecs
#     if key in ["StringEncoding", "IOEncoding"]:
#         encoding = prefClass.settings.value(
#             "System/" + key, prefClass.sysDefaults[key])
#         if encoding not in supportedCodecs:
#             encoding = prefClass.sysDefaults[key]
#         return encoding
#
#
# def setSystem(key, value, prefClass=Prefs):
#     """
#     Module function to store the various system settings.
#
#     @param key the key of the setting to be set
#     @param value the value to be set
#     @param prefClass preferences class used as the storage area
#     """
#     prefClass.settings.setValue("System/" + key, value)
#
#
# def setTemplates(key, value, prefClass=Prefs):
#     """
#     Module function to store the Templates related settings.
#
#     @param key the key of the setting to be set
#     @param value the value to be set
#     @param prefClass preferences class used as the storage area
#     """
#     if key in ["EditorFont"]:
#         prefClass.settings.setValue("Templates/" + key, value.toString())
#     else:
#         prefClass.settings.setValue("Templates/" + key, value)
#
#
# def getPluginManager(key, prefClass=Prefs):
#     """
#     Module function to retrieve the plugin manager related settings.
#
#     @param key the key of the value to get
#     @param prefClass preferences class used as the storage area
#     @return the requested user setting
#     """
#     if key in ["DownloadPath"]:
#         return prefClass.settings.value(
#             "PluginManager/" + key, prefClass.pluginManagerDefaults[key])
#     elif key in ["UpdatesCheckInterval", "KeepGenerations"]:
#         return int(prefClass.settings.value(
#             "PluginManager/" + key, prefClass.pluginManagerDefaults[key]))
#     elif key in ["HiddenPlugins"]:
#         return toList(prefClass.settings.value(
#             "PluginManager/" + key, prefClass.pluginManagerDefaults[key]))
#     else:
#         return toBool(prefClass.settings.value(
#             "PluginManager/" + key, prefClass.pluginManagerDefaults[key]))
#
#
# def setPluginManager(key, value, prefClass=Prefs):
#     """
#     Module function to store the plugin manager related settings.
#
#     @param key the key of the setting to be set
#     @param value the value to be set
#     @param prefClass preferences class used as the storage area
#     """
#     prefClass.settings.setValue("PluginManager/" + key, value)
#

def toBool(value):
    """
    Module function to convert a value to bool.

    @param value value to be converted
    @return converted data
    """
    if value in ["true", "1", "True"]:
        return True
    elif value in ["false", "0", "False"]:
        return False
    else:
        return bool(value)


def toList(value):
    """
    Module function to convert a value to a list.

    @param value value to be converted
    @return converted data
    """
    if value is None:
        return []
    elif not isinstance(value, list):
        return [value]
    else:
        return value


def toByteArray(value):
    """
    Module function to convert a value to a byte array.

    @param value value to be converted
    @return converted data
    """
    if value is None:
        return QByteArray()
    else:
        return value


def toDict(value):
    """
    Module function to convert a value to a dictionary.

    @param value value to be converted
    @return converted data
    """
    if value is None:
        return {}
    else:
        return value
#

# -------------future may be used------------- ↑


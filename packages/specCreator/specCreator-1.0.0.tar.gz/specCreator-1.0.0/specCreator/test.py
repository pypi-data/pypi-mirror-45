#!/usr/bin/env python
# -*- coding=utf-8 -*-


import sys
from Tools.shellCommand import Shell

sys.path.append("../specCreator")

shell = Shell.instance()


def testSpecCreatorMethod(method):
    shell.excommand_until_done("./specCreator.py " + method)

def checkVersion():
    testSpecCreatorMethod("--version")


def checkLibCreate(user, projectPath):
    """
    创建一个项目
    :param user: 用户
    :param projectPath: 即将要创建的项目的目录
    :return:
    """
    testSpecCreatorMethod("libCreate --user=" + user + " --projectPath="+projectPath)


checkVersion()
# checkLibCreate("handa", "~/test/LJABCD")

# testSpecCreatorMethod("supportBinary")
# testSpecCreatorMethod("check")
# testSpecCreatorMethod("package")
    # testSpecCreatorMethod("autoPackage")


#!/usr/bin/env python
# -*- coding=utf-8 -*-


from formatter import Formatter

class Tips(object):
    __instance = None

    def __init__(self):
        self.formatter = Formatter.instance()

    @classmethod
    def instance(cls):
        if cls.__instance is None:
            cls.__instance = Tips()
        return cls.__instance

    def showTips(self):
        tips = """脚本参数错误，请参考以下提示：

            需要先看看相关python环境有没有安装好。请运行
                > specCreator env
            参数：
                --gerritUser            gerrit用户名
                --projectPath           工程地址
                --podName               pod库名（需要再根目录)
                --version               要打包的版本
                --subPackage            打包的时候是否要每个subspec单独打包。（默认为False)
                --commitId              打包的时候依照哪个commit开始打包（这个commitId必须已经push到远程）  
                --debug                 打debug还是release（默认是false，即打release包)
                --dependencyJSON        依赖的库的JSON（字典）,可以是JSON文件的路径
                --moduleSources         组件池，不包括master源，master会内置。
                --updateMasterSource    Bool 值，是否更新master源，默认为false.

                下面的是只在 autoPackage 中起作用，只要有参数就可
                --branch                在哪个分支上打包
                --check                 打包前要检查podspec书写是否规范
                --framework             要打Framework静态库
                --archive               要打Archive静态库
                --debugPackage          打debug包
                --releasePackage        打release包
                --autoPush              打完包后自动commit并push
                --autoPushRepo          提交后自动更新repo发布。如果已经在repo白名单不需要此操作
                --repoSources           repo仓库的url，地址发布到哪个仓库
                --resultPath            必要信息会以JSON格式追加到这个文件
                --subspecs              字符串，需要打的subspec，多个用逗号隔开。前提是subPackage为True.（如果只提供部分subspec，其他的subspec不处理（即如果其他的subspec有静态库，不删除，如果没有，也不会重新打)，适用于做subspec的部分更新，而不需要把没变化的subspec也打静态库，节省时间）



            本脚本的功能：
                1：从0开始创建一个spec标准库模板（暂不支持从一个已经存在的工程创建）
                    > specCreator init 
                        --gerritUser=handa 
                        --projectPath=/Users/handa/Documents/LJABCD
                2：spec标准库检查。
                    > specCreator check
                        --projectPath=/Users/handa/Documents/LJCache 
                        --podName=LJCache 
                        --dependencyJSON="{\"LJHTTPService\":\"0.2.2\",\"AFNetworking\":\"3.2.1\"}"
                3：创建spec标准库的静态库（.framework)
                前提是：有spec工程，且工程里改了spec文件，并检查通过
                    > specCreator package
                        --projectPath=/Users/handa/Documents/LJCache
                        --podName=LJCache
                        --version=0.1.25
                        --commitId=ffa72511e6166222f294ddd874fd54247e82b369
                        --debug=false
                        --dependencyJSON="{\"LJHTTPService\":\"0.2.2\",\"AFNetworking\":\"3.2.1\"}"
                4：创建spec标准库的静态库（.a）（暂不支持生成非标准模板的静态库）
                前提是：有spec工程，且工程里改了spec文件，并检查通过
                    > specCreator packageA
                        --projectPath=/Users/handa/Documents/LJCache
                        --podName=LJCache
                        --version=0.1.25
                        --subPackage=false
                        --commitId=ffa72511e6166222f294ddd874fd54247e82b369
                        --debug=false
                        --dependencyJSON="{\"LJHTTPService\":\"0.2.2\",\"AFNetworking\":\"3.2.1\"}"
                5：对已经存在的podspec文件进行源码和静态库的适配。
                    > specCreator initSpec
                        --projectPath=/Users/handa/Documents/LJABCD
                        --podName=LJABCD

            对服务端如果完全自动化，请运行：
                    > specCreator autoPackage
                        --projectPath=/Users/handa/Documents/LJCache
                        --podName=LJCache
                        --branch=master
                        --version=0.1.27
                        --subPackage=false
                        --commitId=a6c064311553a38d543d7944c07d4643388b0444
                        --dependencyJSON="{\"LJHTTPService\":\"0.2.2\",\"AFNetworking\":\"3.2.1\"}"
                        --resultPath=/Users/handa/Documents/LJCache/result.txt
                        --repoSource=http://git.lianjia.com/mobile_ios/Lianjia_component_Podspec.git
                        --framework
                        --archive
                        --check
                        --debugPackage
                        --releasePackage
                        --autoPush
                        --autoPushRepo
                        --subspecs=Foundation,UIKit,Core

            init 运行前提：
                1：先从张岩松那里申请创建一个girrit项目，从那里获取工程名，如：LJCache

            运行前提灰常重要
        """
        self.formatter.format_info(tips)
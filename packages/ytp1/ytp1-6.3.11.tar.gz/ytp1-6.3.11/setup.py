# encoding:utf-8
import codecs
import os
import platform
import re
import shutil
import sys

#for setup
from setuptools       import setup,find_packages
from Cython.Build     import cythonize,   build_ext
from Cython.Distutils import Extension as Cython_Extension
 
#for copy dir and file
from distutils.dir_util import copy_tree

import importlib,sys
importlib.reload(sys) 

CTP_Version="v6.3.11"
PRJ_NAME="ptp"

arch = platform.architecture()
if arch != "64bit":
    myArch = "64"
elif arch != "32bit":
    myArch = "32"
else:
    raise EnvironmentError("The architecture of platform is error.")

BASE_DIR       = os.path.dirname(os.path.abspath(__file__))
MYCTP_PRJ      = os.path.join(BASE_DIR,  "ptp")
CTP_LIB        = os.path.join(BASE_DIR,  "ctp" , CTP_Version)

C2CYTHON_HEADER = os.path.join(MYCTP_PRJ, "c2cython")
CYTHON2C_HEADER = os.path.join(MYCTP_PRJ, "cython2c")
 
package_data = []
extra_link_args = None
extra_compile_args = None

l_myOS = platform.system()
if l_myOS == "Linux":
    CTP_LIB       = os.path.join(CTP_LIB, "linux" + myArch)
    package_data.append(CTP_LIB + "/*.so")
    extra_compile_args = ["-Wall"]
    extra_link_args = ['-Wl,-rpath,$ORIGIN']
    l_data_files=[(CTP_LIB + "/libthostmduserapi.so"), (CTP_LIB + "/libthosttraderapi.so")]
    
elif l_myOS == "Windows":
    CTP_LIB = os.path.join(CTP_LIB, "windows" + myArch)
    extra_compile_args = ["/GR", "/EHsc"]
    extra_link_args = []
    package_data.append(CTP_LIB + "\\*.dll") 
    l_data_files=[(CTP_LIB + "\\thostmduserapi.dll"), (CTP_LIB + "\\thosttraderapi.dll")]
else:
    print("不支持的操作系统")
    sys.exit(1)

    
########################################    
CTP_HEADER     = CTP_LIB    
#if sys.platform in ["linux", "win32"]:
#    copy_tree(CTP_LIB, MYCTP_PRJ)

common_args = {
    "cython_include_dirs": [CYTHON2C_HEADER, C2CYTHON_HEADER],
    "include_dirs": [CTP_HEADER, C2CYTHON_HEADER],
    "library_dirs": [CTP_LIB],
    "language": "c++",
    "extra_compile_args": extra_compile_args,
    "extra_link_args": extra_link_args,
}
# cython: binding=True
# binding = true for inspect get callargs
'''
c 和 python 混合编程
sources=[
            'krahenbuhl2013.pyx',
            "src/densecrf.cpp", 
        ]
'''
l_setup_ext_modules = cythonize([Cython_Extension(name=PRJ_NAME + ".MdApi",
                                                     sources=[ PRJ_NAME + "/MdApi.pyx"],
                                                     libraries=["thostmduserapi"],
                                                     **common_args),
                                 Cython_Extension(name=PRJ_NAME + ".TraderApi",
                                                     sources=[PRJ_NAME + "/TraderApi.pyx"],
                                                     libraries=["thosttraderapi"],
                                                     **common_args)
                                ],
                                compiler_directives={'language_level': 3,"binding": True}
                                )

l_setup_description                   = '利用python封装了CTP的动态链接库，方便python的童鞋调用' #程序的简单描述
l_setup_long_description_content_type = 'text/markdown',
l_setup_long_description              = codecs.open("README.md", encoding="utf-8").read() #程序的详细描述
l_setup_url                           = "https://github.com/datamgr/ptp"#程序的官网地址
l_setup_keywords                      = "SimNow,CTP,Future,SHFE,Shanghai Future Exchange"#程序的关键字列表

#对于简单工程来说，手动增加packages参数很容易，刚刚我们用到了这个函数，它默认在和setup.py同一目录下搜索各个含有 __init__.py的包。
#其实我们可以将包统一放在一个src目录中，另外，这个包内可能还有aaa.txt文件和data数据文件夹。另外，也可以排除一些特定的包
#find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])
#需要打包的目录列表
l_setup_package_data      = {"": []}#{"": package_data}#通常包含与包实现相关的一些数据文件、dll文件或者类似于readme的文件
#package_data = {'': ['*.txt'], 'mypkg': ['data/*.dat'],}

l_setup_packages          = ["pymysql","ptp"]#find_packages(["*pymysql*","*python_ctp*"]) 
l_setup_py_modules        = ""#需要打包的python文件列表
l_setup_download_url      = l_setup_url#程序的下载地址
l_setup_cmdclass          = {'build_ext': build_ext}#
l_setup_data_files        = l_data_files#打包时需要打包的数据文件，如图片，配置文件等
l_setup_scripts           = ""#安装时需要执行的脚步列表
l_setup_package_dir       = ""#告诉setuptools哪些目录下的文件被映射到哪个源码包。一个例子：package_dir = {'': 'lib'}，表示“root package”中的模块都在lib 目录中。
l_setup_requires = ""#定义依赖哪些模块 
l_setup_provides = ""#定义可以为哪些模块提供依赖 

l_setup_install_requires = ""#["requests"] 需要安装的依赖包
l_setup_include_dirs     = [CTP_HEADER, CYTHON2C_HEADER]#
# 添加这个选项，在windows下Python目录的scripts下生成exe文件
# 注意：模块与函数之间是冒号:
l_setup_entry_points={'console_scripts': [
              'redis_run = RedisRun.redis_run:main',
               ]
             }

##########################################
#以下基本不需要变化             
l_setup_python_requires   = ">=3.5"
#l_setup_name              = PRJ_NAME + '_' + l_myOS        #包名称
l_setup_name              = 'ytp1'       #包名称
l_setup_version           = CTP_Version      #包版本
l_setup_author            = 'liu.changsheng' #程序的作者
l_setup_author_email      = '19578602@qq.com'#程序的作者的邮箱地址
l_setup_maintainer        = 'liu.changsheng' #维护者
l_setup_maintainer_email  = '19578602@qq.com'#维护者的邮箱地址
l_setup_license           = "LGPLv3"  #程序的授权信息
l_setup_platforms         = ["win32", "linux"]#程序适用的软件平台列表
# 程序的所属分类列表
l_setup_classifiers=[
        "Development Status ::  - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: POSIX",
        "Operating System :: Microsoft",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries"
    ]
# 此项需要，否则卸载时报windows error
l_setup_zip_safe=False 

   
setup(
    name                          =l_setup_name,
    version                       =l_setup_version,
    description                   =l_setup_description,
    long_description              =l_setup_long_description,
    long_description_content_type =l_setup_long_description_content_type,
    license                       = l_setup_license,
    keywords                      = l_setup_keywords,
    author                        = l_setup_author,
    author_email                  = l_setup_author_email,
    url                           = l_setup_url,
    include_dirs                  = l_setup_include_dirs,
    platforms                     = l_setup_platforms,
    packages                      = l_setup_packages,
    #package_data                  = l_setup_package_data,
    data_files                    = l_setup_data_files,
    python_requires               = l_setup_python_requires,    
    ext_modules                   = l_setup_ext_modules,
    cmdclass                      = l_setup_cmdclass,
    entry_points                  = l_setup_entry_points,
    classifiers                   = l_setup_classifiers,
    zip_safe                      = l_setup_zip_safe
)
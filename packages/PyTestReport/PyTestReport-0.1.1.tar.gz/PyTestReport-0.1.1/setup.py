#!/usr/bin/env python
# coding=utf-8
from setuptools import setup, find_packages

# python setup.py sdist
# python setup.py bdist
# python setup.py bdist_egg
# python setup.py bdist_wheel

setup(
    name="PyTestReport",
    version="0.1.1",
    keywords=("test report", "python unit testing"),
    description="The HTML Report for Python unit testing Base on HTMLTestRunner",
    long_description="The HTML Report for Python unit testing Base on HTMLTestRunner",
    license="GPL V3",

    url="https://github.com/five3/PyTestReport",
    author="Xiaowu Chen",
    author_email="five3@163.com",

    package_dir={'pytestreport': 'pytestreport'},         # 指定哪些包的文件被映射到哪个源码包
    packages=['pytestreport'],       # 需要打包的目录。如果多个的话，可以使用find_packages()自动发现
    include_package_data=True,
    py_modules=[],          # 需要打包的python文件列表
    data_files=['pytestreport/templates/default.html', 'pytestreport/static/css/default.css', 'pytestreport/static/js/default.js'],          # 打包时需要打包的数据文件
    platforms="any",
    install_requires=[      # 需要安装的依赖包
        'Flask>=1.0.2'
    ],
    scripts=[],             # 安装时需要执行的脚本列表
    entry_points={
        'console_scripts': [    # 配置生成命令行工具及入口
            'PyTestReport.shell = pytestreport:shell',
            'PyTestReport.web = pytestreport:web'
        ]
    },
    classifiers=[           # 程序的所属分类列表
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    zip_safe=False
)

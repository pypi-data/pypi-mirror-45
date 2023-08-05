#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: lcylmhlcy
# Mail: lcylmhlcy@163.com
# Created Time:  2019-04-03 19:45:00 PM
#############################################


from setuptools import setup, find_packages

setup(
    name = "MailModel",
    version = "0.1.1",
    keywords = ("pip", "mailtool", "modeltrain"),
    description = "mail to tell model situation",
    long_description = "mail to tell model training situation",
    license = "MIT Licence",

    url = "https://github.com/lcylmhlcy/MailModel",
    author = "lcylmhlcy",
    author_email = "lcylmhlcy@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['chardet'],
    python_requires=">=3.6"
)
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2013, Cameron White
import setuptools

if __name__ == "__main__":
    setuptools.setup(
        name="acmbot",
        version='0.1.0',
        description="A bot for @pdxacm",
        author="Cameron Brandon White",
        author_email="cameronbwhite90@gmail.com",
        provides=[
            "acmbot",
        ],
        packages=[
            "modules",
        ],
        py_modules = [
            "bot",
        ],
        package_data = {
            'PyOLP': ["LICENSE", "README.md", "config.cfg"],
        },
        install_requires = [
            'kitnirc',
            'pyyaml',
            'nose',
        ],
        include_package_data=True,
    )

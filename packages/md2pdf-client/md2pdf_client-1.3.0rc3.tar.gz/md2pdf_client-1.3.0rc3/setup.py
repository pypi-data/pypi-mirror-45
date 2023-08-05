#! /usr/bin/env python3
import os
import subprocess
from setuptools import setup, find_packages
import re

package_name = 'md2pdf_client'
filename = os.path.join(package_name, (package_name + '.py'))


def describe_write_version():
    # Use git describe to get current version identifier
    git_describe = subprocess.check_output(
        'git describe --tags --dirty --abbrev=4',
        shell=True
    ).decode('UTF-8')
    describe_re = re.compile('(v\d+\.\d+\.\d+\.?[abrc]{1,2}\d{0,3})\-?(\d+)?\-?(g[a-zA-Z0-9]+)?')
    describe_search = re.search(describe_re, git_describe)
    if describe_search:
        full_tag = describe_search.group(1)
        full_tag = full_tag.replace('v','')
        dev_num = describe_search.group(2)
        local_tag = describe_search.group(3)
        try:
            if git_describe.index('dirty'):
                dirty = True
        except ValueError:
            dirty = False
        if dev_num:
            full_tag += ".dev"
            full_tag += dev_num
            if dirty:
                full_tag += "+"
                full_tag += local_tag
                full_tag += ".dirty"
        elif dirty:
            full_tag += "+dirty"

    # Write out version name to __version__.py in the same directory as package source
    for directory, _, filenames in os.walk(os.getcwd()):
        if (package_name + '.py') in filenames:
            ver_filename = os.path.join(directory, '__version__.py')
            try:
                os.unlink(ver_filename)
            except FileNotFoundError:
                pass
            with open(ver_filename, 'wt', encoding='UTF-8') as ver_file:
                ver_file.write('version = "{}"\n'.format(full_tag))

    return full_tag


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name=package_name,
    version=describe_write_version(),
    author='Sean Lanigan',
    description='Client for using an md2pdf server to render Markdown text into a pretty PDF',
    url='https://gitlab.com/md2x/md2pdf-client',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=[package_name],
    entry_points={
        'console_scripts': [
            'md2pdf-client = md2pdf_client.md2pdf_client:main'
        ]
    },
    packages=find_packages(),
    license='GNU Affero General Public License v3 or later',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Topic :: Office/Business",
        "Intended Audience :: End Users/Desktop"
    ],
)

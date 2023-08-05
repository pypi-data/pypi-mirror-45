#!/usr/bin/python2
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import re

with open('pythonvideoannotator/__init__.py', 'r') as fd:
    content = fd.read()
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', content, re.MULTILINE).group(1)

setup(
    name='Python video annotator',
    version=version,
    description="""""",
    author=['Ricardo Ribeiro'],
    author_email='ricardojvr@gmail.com',
    url='https://bitbucket.org/fchampalimaud/pythonvideoannotator-models',
    packages=find_packages(),
    install_requires=[
        'simplejson',
        'pypi-xmlrpc',
        'send2trash',
        'scipy',
        'sklearn',
        'confapp',
        'pyforms-gui',
        'mcv-gui==0.1',
        'geometry-designer==0.1',
        'modular-computer-vision-api==0.1',
        'modular-computer-vision-api-gui==0.1',
        'python-video-annotator-models==0.1',
        'python-video-annotator-models-gui==0.1',
        'python-video-annotator-module-tracking==0.2',
        'python-video-annotator-module-eventstats==0.1',
        'python-video-annotator-module-import-export==0.1',
        'python-video-annotator-module-regions-filter==0.1',
        'python-video-annotator-module-background-finder==0.1',
        'python-video-annotator-module-virtual-object-generator==0.1',
        'python-video-annotator-module-timeline==0.2',
        'python-video-annotator-module-smooth-paths==0.1',
        'python-video-annotator-module-motion-counter==0.1',
        'python-video-annotator-module-create-paths==0.1',
        'python-video-annotator-module-path-editor==0.1',
        'python-video-annotator-module-distances==0.1',
        'python-video-annotator-module-find-orientation==0.1',
        'python-video-annotator-module-contours-images==0.1',
        'python-video-annotator-module-path-map==0.1'
    ],
    entry_points={
        'console_scripts': [
            'start-video-annotator=pythonvideoannotator.__main__:start',
        ],
    },
    package_data={'pythonvideoannotator': [
        'resources/icons/*.png',
        'resources/themes/default/*.css',
        ]
    },
)

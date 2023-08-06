#!/usr/bin/env python

from distutils.core import setup

setup(
        name='tapconverter',
        version='0.1',
        description='Converter from Cram (and some other formats) to TAP',
        py_modules = ['tapconverter'],
        scripts = [
            'scripts/cram2tap',
            'scripts/junit2tap',
            'scripts/nose2tap',
            ],
        author = 'Nikolaus Schueler',
        author_email = 'nik@drnik.org',
        )

# vim: ai ts=4 sts=4 et sw=4 ft=python

# -*- coding: utf-8 -*-
import os

import setuptools
import sys

try:
    from pip import download
    from pip import req
except ImportError as e:
    from pip._internal import download
    from pip._internal import req


HERE = os.path.abspath(os.path.dirname(__file__))


def get_requirements(reqfile):
    path = os.path.join(HERE, reqfile)
    deps = list()
    for dep in req.parse_requirements(path, session=download.PipSession()):
        try:
            # Pip 8.1.2 Compatible
            specs = ','.join(''.join(str(spec)) for spec in dep.req.specifier)
        except AttributeError:
            # Pip 1.5.4 Compatible
            specs = ','.join(''.join(spec) for spec in dep.req.specs)
        requirement = '{name}{extras}{specs}'.format(
            name=dep.name,
            extras=(
                '[{extras}]'.format(extras=','.join(dep.extras))
                if dep.extras else ''
            ),
            specs=specs,
        )

        deps.append(requirement)
    return deps

with open('README.md', 'r') as fh:
    long_description = fh.read()


setuptools.setup(
    name='dojot-flow-node',
    description='Dojot flow node.',
    long_description=long_description,
    version='0.0.7',

    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=get_requirements('requirements.txt'),

    author='Fabio Beranizo Fontes Lopes',
    author_email='fabiol@cpqd.com.br',
    url='http://dojot.com.br',
)
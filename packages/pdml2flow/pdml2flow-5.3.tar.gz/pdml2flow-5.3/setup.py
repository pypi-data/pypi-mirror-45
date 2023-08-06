# vim: set fenc=utf8 ts=4 sw=4 et :
import os
import tarfile

from setuptools import setup, find_packages

# I really prefer Markdown to reStructuredText. PyPi does not.
# from: https://coderwall.com/p/qawuyq/use-markdown-readme-s-in-python-modules
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst', format='markdown')
    long_description = long_description.replace('\r','')
    with open('README.rst', 'w') as f:
        f.write(long_description)
except (OSError, ImportError):
    print('Pandoc not found. Long_description conversion failure.')
    # pandoc is not installed, fallback to using raw contents
    with open('README.md', 'r') as f:
        long_description = f.read()

# Setup the project
setup(
    name = 'pdml2flow',
    keywords = 'wireshark pdml flow aggregation plugins',
    version = '5.3',
    packages = find_packages(exclude=['test']),
    install_requires = [
        'typing',
        'dict2xml'
    ],
    # other arguments here...
    entry_points={
        'console_scripts': [
            'pdml2flow = pdml2flow:pdml2flow',
            'pdml2frame = pdml2flow:pdml2frame',
            'pdml2flow-new-plugin = pdml2flow:pdml2flow_new_plugin',
        ],
        'pdml2flow.plugins.base': [
            'json = pdml2flow.plugins.json_output:JSONOutput',
            'xml = pdml2flow.plugins.xml_output:XMLOutput',
        ]
    },
    # metadata
    author = 'Mischa Lehmann',
    author_email = 'ducksource@duckpond.ch',
    description = 'Aggregates wireshark pdml to flows',
    long_description = long_description,
    include_package_data = True,
    license = 'Apache 2.0',
    url = 'https://github.com/Enteee/pdml2flow',
)

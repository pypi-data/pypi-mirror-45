from setuptools import setup
from upnpy import __author__, __author_email__, __project_url__, __version__, __description__

setup(
    name='UPnPy',
    version=__version__,
    packages=['tests', 'upnpy', 'upnpy.soap', 'upnpy.soap.ServiceTemplates', 'upnpy.ssdp', 'upnpy.upnp'],
    keywords=['upnp', 'upnpy'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    url=__project_url__,
    license='MIT',
    author=__author__,
    author_email=__author_email__,
    description=__description__
)

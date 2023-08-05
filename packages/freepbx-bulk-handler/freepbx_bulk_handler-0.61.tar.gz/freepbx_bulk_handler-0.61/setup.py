from setuptools import setup, find_packages

__author__ = "Dax Mickelson"
__author_email = "daxm@daxm.net"
__license__ = "BSD"

setup(
    name='freepbx_bulk_handler',
    version='0.61',
    description="Assist administrators of FreePBX systems when they need to use the Bulk Handler module",
    long_description="""This python package is designed to assist administrators of FreePBX systems when
they need to use the Bulk Handler module.""",
    url='https://gitlab.com/daxm/FreePBX_Bulk_Handler',
    author='Dax Mickelson',
    author_email='daxm@daxm.net',
    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Other Audience',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Programming Language :: Python :: 3.6',
        'Topic :: Communications',
        'Topic :: Communications :: Telephony',
        'Topic :: Communications :: Internet Phone',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    keywords='FreePBX, bulk handler, freepbx',
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=[],
    python_requires='>=3.6',
    package_data={},
    data_files=None,
)
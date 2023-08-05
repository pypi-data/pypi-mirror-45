import os
from distutils.core import setup

with open('README', 'r') as fh:
    long_description = fh.read()

if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
else:
    version = os.environ.get('CI_JOB_ID', os.environ.get('CI_COMMIT_SHORT_SHA', '0.1.0'))

setup(
    name='file_organizer_cli',
    packages=[
        'file_organizer_cli',
        'file_organizer_cli.utils'
    ],
    version=version,
    license='gpl-3.0',
    description='interactive file extension manager cli',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Philipp Zettl',
    author_email='philipp.zettl@time-dev.de',
    url='https://gitlab.com/philsupertramp/file-organizer-cli',
    download_url='https://gitlab.com/philsupertramp/file-organizer-cli/-/archive/master/file-organizer-cli-master.tar.gz',
    install_requires=[
        'PyInquirer',
    ],
    requires=[
        'PyInquirer',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)

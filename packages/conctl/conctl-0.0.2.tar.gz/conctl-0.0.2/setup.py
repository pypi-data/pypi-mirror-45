from distutils.core import setup


setup(
    name='conctl',
    version='0.0.2',
    url='https://github.com/joedborg/conctl',
    license='Apache License 2.0',
    author='Joe Borg',
    author_email='joe@josephb.org',
    description='Drive Containerd and Docker from one CLI',
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'conctl=conctl:cli',
        ],
    }
)

from distutils.core import setup

VERSION = '1.0.5'

setup(
    name='InANutshell',
    version=VERSION,
    author='Josh Prakke',
    author_email='joshprakke@gmail.com',
    url='https://github.com/JPrakke/in-a-nutshell',
    install_requires=['pyperclip == 1.7.0',],
    packages=['nutshell',],
    license='MIT License',
    description='makes meme text',
    long_description=open('README.txt').read(),
    entry_points = {
        'console_scripts':[
            'nutshell=nutshell.nutshell:run'
        ]
    }
)
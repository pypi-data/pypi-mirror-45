from distutils.core import setup

setup(
    name='ztctl',
    packages=['ztctl'],
    version='0.3',
    license='MIT',
    description='Zerotier controller bindings for python',
    author='Valtýr Örn Kjartansson',
    author_email='valtyr@gmail.com',
    url='https://github.com/valtyr/ztctl',
    download_url='https://github.com/valtyr/ztctl/archive/v0.3.tar.gz',
    keywords=['zerotier', 'zerotier-cli', 'ztctl'],
    install_requires=[
        'aiohttp==3.5.4',
        'async-timeout==3.0.1',
        'attrs==19.1.0',
        'chardet==3.0.4',
        'decorator==4.4.0',
        'idna==2.8',
        'ipdb==0.12',
        'ipython-genutils==0.2.0',
        'multidict==4.5.2',
        'prompt-toolkit==2.0.9',
        'ptyprocess==0.6.0',
        'Pygments==2.3.1',
        'six==1.12.0',
        'traitlets==4.3.2',
        'wcwidth==0.1.7',
        'yarl==1.3.0',
    ],
    classifiers=[
        # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        # Language support
        'Programming Language :: Python :: 3.6',
    ],
)

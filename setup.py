from distutils.core import setup
setup(
        setup_requires=['setuptools_scm'],
        include_package_data=True,
        name="FileOrganiser",
        packages=["FileOrganiser"],
        version='1.0.6',
        license='idgaf',
        description='A Modular tool to keep directories organised',
        author='Ellie Mae Galyean',
        author_email='tggalyea@uncg.edu',
        url='https://github.com/lifesgood123/FileOrganiser',
        download_url =
        'https://github.com/Lifesgood123/FileOrganiser/archive/refs/tags/1.0.5.tar.gz',
        keywords = ['files', 'organisation', 'productivity',
            'daemon'],
        install_requires = [
                'watchdog',
                'toml'
            ],
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: End Users/Desktop',      # Define that your audience are developers
            'License :: Freely Distributable',   # Again, pick a license
            'Programming Language :: Python :: 3.8',
            ]
        )


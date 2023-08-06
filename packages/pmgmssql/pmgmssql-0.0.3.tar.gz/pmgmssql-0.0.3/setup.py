import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="pmgmssql",
    version="0.0.3",
    author="Preston Meyer Group",
    author_email="dev@pmgroup.ch",
    description="PMG MS SQL Server Toolbox",
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        #'Operating System :: OS Independent',
        'Operating System :: POSIX :: Linux',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Database'
    ],
    py_modules=['pmgmssql'],
    install_requires=open('requirements.txt', 'r').read(),
    python_requires='~=3.6'
)

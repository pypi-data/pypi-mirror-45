from setuptools import setup

setup(
        name='cobjects',
        version='0.0.9',
        description='Manage C data from Python for C libraries',
        author='Riccardo De Maria',
        author_email='riccardo.de.maria@cern.ch',
        url='https://github.com/rdemaria/cobjects',
        python_requires='>=3.6',
        packages=['cobjects','src','_cffi_builder'],
        package_dir={'cobjects': 'cobjects'},
        cffi_modules=["_cffi_builder/cbuffer_builder.py:ffibuilder"],
        package_data={'src':['*.h']},
        install_requires=['numpy','cffi>=1.0.0'],
        setup_requires=['cffi>=1.0.0'],
)



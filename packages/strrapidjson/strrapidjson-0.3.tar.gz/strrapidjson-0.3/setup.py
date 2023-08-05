from setuptools import setup, Extension

setup(
    name='strrapidjson',
    version='0.3',
    description='Python 2 rapidjson wrapper that does not use unicode objects',
    long_description=open('README.rst').read(),
    license='MIT',
    author='Levon Budagyan',
    author_email='levon@aarki.com',
    url='https://github.com/aarki/strrapidjson',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: C++',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
    ],
    keywords='json rapidjson',
    ext_modules=[
        Extension('strrapidjson',
            sources=['pyrapidjson/_pyrapidjson.cpp'],
            include_dirs=['./pyrapidjson/rapidjson/include/'],
        )]
)

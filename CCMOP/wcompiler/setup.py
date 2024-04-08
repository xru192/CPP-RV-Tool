from setuptools import setup, find_packages

setup(
    name='wcompiler',
    version='0.0.5',

    include_package_data=True,

    packages=find_packages(),

    entry_points = {
        'console_scripts': [
            'wac = wac.wac:main',
            'wacc = wac.aspect.wacc:main',
            'wacxx = wac.aspect.wacxx:main',
            'war=wac.aspect.wacar:main'
        ],
    },
)

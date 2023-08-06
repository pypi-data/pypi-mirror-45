from setuptools import setup

setup(
    name='mgrep',
    version='0.1.2',
    py_modules=['mgrep'],
    install_requires=[
        'Click',
    ],
    python_requires='>=3.4',
    entry_points='''
        [console_scripts]
        mgrep=mgrep:cli
    ''',
)

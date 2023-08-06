from setuptools import setup


try:
    from mgrep import __version__ as version
except ImportError:
    import re
    pattern = re.compile(r"__version__ = '(.*)'")
    with open('mgrep.py') as f:
        version = pattern.search(f.read()).group(1)


setup(
    name='mgrep',
    version=version,
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

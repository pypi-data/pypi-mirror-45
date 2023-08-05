import os

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension


TELECOM_NATIVE_DIR = os.getenv('TELECOM_NATIVE_DIR', '../cmd/telecom-native/')


telecom_module = Extension(
    'telecom.telecom',
    include_dirs=[TELECOM_NATIVE_DIR],
    libraries=['telecom'],
    library_dirs=[TELECOM_NATIVE_DIR],
    sources=['telecom.c'],
)

setup(
    name='telecom-py',
    version='0.0.1',
    author='b1nzy',
    author_email='b1naryth1ef@gmail.com',
    description='Discord voice client',
    url='https://github.com/b1naryth1ef/telecom',
    packages=['telecom'],
    ext_modules=[telecom_module],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    classifiers=[
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Programming Language :: C',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)

import os
from subprocess import Popen, PIPE

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = ""

with open('requirements.txt') as f:
    required = f.read().splitlines()

for i, l in enumerate(required):
    if l.startswith('git'):
        if 'ProjectUtils' in l:
            required[i] = 'rutils@' + l
        elif 'ProjectsC' in l:
            required[i] = 'rprojc@' + l




def get_git_version(default="0.0.1"):
    try:
        p = Popen(['git', 'describe', '--tags'], stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        line = p.stdout.readlines()[0]
        line = line.strip()
        return line.decode()
    except:
        return default

setup(
    name='cspatterns',
    version=get_git_version(default="0.0.1"),
    classifiers=[
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.7'],
    url='https://github.com/romanchyla/CSPatterns',
    license='MIT',
    author="rc",
    description='Library of toy datastructures and algs, for experimentation purposes only',
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=required
  )

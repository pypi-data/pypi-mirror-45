import os
import re
from setuptools import setup, find_packages
from setuptools.command.install_scripts import install_scripts

VERSION="1.1.5.dev1"

class my_install_scripts(install_scripts):
  def write_script(self, script_name, contents, mode="t", *ignored):
    contents = re.sub("import sys",
                      "import sys\nsys.path.append('/opt/graphite/lib')",
                      contents)
    install_scripts.write_script(self, script_name, contents, mode="t", *ignored)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="carbonate3",
    version=VERSION,
    maintainer="Alex Klimenka",
    maintainer_email="nimda7@gmail.com",
    description="Tools for managing federated carbon clusters.",
    license="MIT",
    keywords="graphite carbon",
    url="https://github.com/nimda7/carbonate3",
    include_package_data=True,
    packages=find_packages(),
    long_description = read('README.md'),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Systems Administration',
    ],
    install_requires=[
      "carbon",
      "whisper",
    ],
    cmdclass={'install_scripts': my_install_scripts},
    entry_points={
        'console_scripts': [
            'carbon-lookup = carbonate.cli:carbon_lookup',
            'carbon-sync = carbonate.cli:carbon_sync',
            'carbon-sieve = carbonate.cli:carbon_sieve',
            'carbon-list = carbonate.cli:carbon_list',
            'carbon-hosts = carbonate.cli:carbon_hosts',
            'carbon-path = carbonate.cli:carbon_path',
            'carbon-stale = carbonate.cli:carbon_stale',
            'whisper-fill = carbonate.cli:whisper_fill',
            'whisper-aggregate = carbonate.cli:whisper_aggregate'
            ]
        }
    )

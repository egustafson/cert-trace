#
# Copyright 2020 Eric Gustafson
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cert-trace",
    version="0.9.0",
    author="Eric Gustafson",
    author_email="eg-git@elfwerks.org",
    description="x509 certificate chain tracing tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/egustafson/cert-trace",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'cert-trace = cert_trace.__main__:main',
        ],
    },
)

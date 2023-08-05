"""Setup file
"""


import setuptools
import pelican_cite_nice


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(name='pelican_cite_nice',
                 version=pelican_cite_nice.__version__,
                 description='Pelican cite plugin modified to work with nice-blog theme',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url=pelican_cite_nice.__github_url__,
                 author='James W. Kennington',
                 author_email='jameswkennington@gmail.com',
                 license='MIT',
                 packages=setuptools.find_packages(),
                 zip_safe=False)

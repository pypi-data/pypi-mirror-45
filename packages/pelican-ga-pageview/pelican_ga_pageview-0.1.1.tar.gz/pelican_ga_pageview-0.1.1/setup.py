"""Setup file
"""

import setuptools
import pelican_ga_pageview

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='pelican_ga_pageview',
                 version=pelican_ga_pageview.__version__,
                 description='Pelican google analytics plugin modified to work with nice-blog theme',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url=pelican_ga_pageview.__github_url__,
                 author='James W. Kennington',
                 author_email='jameswkennington@gmail.com',
                 license='MIT',
                 packages=setuptools.find_packages(),
                 zip_safe=False)

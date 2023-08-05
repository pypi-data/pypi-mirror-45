"""Setup file
"""


import setuptools
import pelican_github_activity


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(name='pelican_github_activity',
                 version=pelican_github_activity.__version__,
                 description='Pelican github activity modified to work with nice-blog theme',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url=pelican_github_activity.__github_url__,
                 author='James W. Kennington',
                 author_email='jameswkennington@gmail.com',
                 license='MIT',
                 packages=setuptools.find_packages(),
                 zip_safe=False)

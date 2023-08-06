# import setuptools
#
# with open("README.md", "r") as fh:
#     long_description = fh.read()
#
# setuptools.setup(
#     name="yuejzDemo",
#     version="0.0.2",
#     author="YueJZ",
#     author_email="yuejianzhong@sensorsdata.cn",
#     description="This is my demo",
#     long_description=long_description,
#     long_description_content_type="text/markdown",
#     url="https://github.com/YueJZSensorsData/FirstDemo",
#     packages=['SADemo'],
# )

from distutils.core import setup

setup(
    name='yuejzDemo',
    version='0.0.5',
    author='YueJZ',
    author_email='yuejianzhong@sensorsdata.cn',
    url='https://github.com/YueJZSensorsData/FirstDemo',
    license='LICENSE.txt',
    packages=['SADemo'],
    description='This is my demo',
    long_description=open('README.txt').read(),

)

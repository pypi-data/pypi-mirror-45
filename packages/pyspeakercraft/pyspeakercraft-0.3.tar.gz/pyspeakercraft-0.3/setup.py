import setuptools

VERSION = '0.3'

setuptools.setup(
    name="pyspeakercraft",
    version="0.3",
    author="BLeBlanc",
    description="Speakercraft MZC controller",
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=['construct','pyserial']
)

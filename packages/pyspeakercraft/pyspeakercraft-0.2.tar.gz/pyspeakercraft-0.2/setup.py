import setuptools

VERSION = '0.2'

setuptools.setup(
    name="pyspeakercraft",
    version="0.2",
    author="BLeBlanc",
    description="Speakercraft MZC controller",
    license='MIT',    
    install_requires=['construct','pyserial']
)

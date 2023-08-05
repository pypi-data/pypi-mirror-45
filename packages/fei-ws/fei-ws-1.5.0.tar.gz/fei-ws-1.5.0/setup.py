from setuptools import setup, find_packages
import fei_ws

setup(
    name='fei-ws',
    version=fei_ws.__version__,
    keywords='fei webservice client',
    author='Arend H. Tolner',
    author_email='arie@scgvisual.com',
    packages=find_packages(exclude=['tests']),
    install_requires=['zeep==3.2.0', 'six==1.12.0'],
    url='http://www.bounder.nl/',
    license='Mozilla Public License 2.0',
    description='Wrapper for the FEI Web Services v1.2',
    long_description=open('README.txt').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3',
    ]
)

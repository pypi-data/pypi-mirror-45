""" See [1] on how to write proper `setup.py` script.

[1] https://github.com/pypa/sampleproject/blob/master/setup.py
"""


from setuptools import setup, find_packages
from tutti_language_detector import __version__


setup(
    name='tutti_language_detector',
    version=__version__,
    description='A tutti specific language detector.',
    long_description='A pre-trained language detection model for tutti.ch ads.',
    author='Oscar Saleta',
    author_email='oscar@tutti.ch',
    license='Proprietary',
    keywords=['language', 'detector'],
    packages=find_packages(exclude=['contrib', 'docs', '*test*']),
    python_requires='>=3.5.2',
    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn',
    ],
    zip_safe=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ],
    include_package_data=True
)

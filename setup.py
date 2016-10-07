from wagtailextras import __version__
from setuptools import setup, find_packages

setup(
    name='wagtailextras',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    # package_dir={'': 'src'},
    url='https://github.com/sinnwerkstatt/wagtailextras',
    keywords="wagtail",
    license='LGPL',
    author='Andreas Nüßlein',
    author_email='andreas.nuesslein@sinnwerkstatt.com',
    install_requires=[
      'wagtail',
    ],
    description='A bunch of little Wagtail helpers',
    classifiers= [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ]
)
from setuptools import setup

setup(
    name='rjango_core',
    version='0.1.1',
    description='Core utilities to enable minimal working Rjango style backends.',
    long_description='',
    author='Nicholas Romero',
    author_email='ncrmro@gmail.com',
    license='MIT License',
    packages=['rjango.core'],
    zip_safe=False,
    install_requires=[
        "django >=2"
    ]
)

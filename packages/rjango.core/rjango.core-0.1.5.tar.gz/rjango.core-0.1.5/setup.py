from setuptools import setup, find_namespace_packages

setup(
    name='rjango.core',
    version='0.1.5',
    package_dir={'': 'src'},
    packages=find_namespace_packages(where='src'),
    description='Utilities to enable minimal working Rjango style backends.',
    long_description='',
    author='Nicholas Romero',
    author_email='ncrmro@gmail.com',
    license='MIT License',
    zip_safe=False,
    install_requires=[
        "django>=2",
        "channels>=2",
        "daphne>=2.2.5,<=2.3.0",
        "whitenoise>=4"
    ]
)

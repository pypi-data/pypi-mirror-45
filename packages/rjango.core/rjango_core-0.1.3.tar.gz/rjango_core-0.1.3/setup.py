from setuptools import setup

setup(
    name='rjango_core',
    version='0.1.3',
    description='Core utilities to enable minimal working Rjango style backends.',
    long_description='',
    author='Nicholas Romero',
    author_email='ncrmro@gmail.com',
    license='MIT License',
    packages=[
        'rjango.core',
        'rjango.core.settings'
    ],
    zip_safe=False,
    install_requires=[
        "django>=2",
        "channels>=2",
        "daphne>=2.2.5,<=2.3.0",
        "whitenoise>=4"
    ]
)

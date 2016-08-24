from setuptools import setup

setup(
    name='FlaskTask',
    version='1.0',
    long_description=__doc__,
    packages=['FlaskTask'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask==0.10.1',
        'Flask-Script==2.0.5',
    ],

)

from distutils.core import setup

setup(
    name='ybc_calculate',
    version='1.0.5',
    description='提供口算相关功能',
    long_description='提供口算相关功能，包括口算批改等',
    author='lanbo',
    author_email='lanbo@fenbi.com',
    keywords=['pip3', 'python3', 'python'],
    url='http://pip.zhenguanyu.com/',
    packages=['ybc_calculate'],
    package_data={'ybc_calculate': ['*.py', '*.png', 'test.*']},
    license='MIT',
    install_requires=[
        'ybc_config',
        'ybc_exception',
        'requests'
    ],
)

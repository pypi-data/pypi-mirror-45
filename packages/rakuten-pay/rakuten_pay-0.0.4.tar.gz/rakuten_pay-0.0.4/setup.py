import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='rakuten_pay',
    version='0.0.4',
    url='https://github.com/ivcmartello/rakuten_pay',
    license='MIT License',
    author='Ivan Carlos Martello',
    author_email='ivcmartello@gmail.com',
    keywords='rakuten pay payment pagamento ecommerce',
    description=u'Rackuten Pay Package',
    packages=setuptools.find_packages(),
    install_requires=['requests'],
)
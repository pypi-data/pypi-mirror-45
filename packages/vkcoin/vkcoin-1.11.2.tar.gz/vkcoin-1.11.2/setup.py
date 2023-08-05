import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='vkcoin',
    version='1.11.2',
    author="crinny",
    author_email="isfellop@gmail.com",
    description="Враппер для платёжного API VK Coin",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/crinny/vkcoin",
    packages=['vkcoin'],
    install_requires=['requests', 'websocket_client', 'vk'],
    classifiers=['Programming Language :: Python :: 3.6'],
)

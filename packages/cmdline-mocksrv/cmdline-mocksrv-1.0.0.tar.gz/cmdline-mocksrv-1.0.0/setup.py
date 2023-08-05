from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='cmdline-mocksrv',
    version='1.0.0',
    author="Nikita Tarasov",
    author_email="mail@ntarasov.ru",
    description="Mocking service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nntarasov/mocksrv",
    packages={'mocksrv', 'mocksrv.configurator', 'mocksrv.handlers', 'mocksrv.router'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask', 'pathvalidate'
    ],
)

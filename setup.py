from setuptools import setup, find_packages

setup(
    name="mock_facebook_app",
    version="1.0",
    description="A mock facebook app",
    author='Dione Marcian Uy',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=['setuptools'],
)

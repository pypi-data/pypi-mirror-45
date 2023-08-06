from setuptools import setup, find_namespace_packages

"""
python setup.py bdist_wheel 生成 wheel文件
python setup.py sdist 生成压缩包
twine upload dist/*
"""
setup(
    name="treelab",
    version="1.1.3",
    package_dir={'': 'treelab-sdk'},
    packages=find_namespace_packages(where='treelab-sdk'),
    install_requires=['Rx>=3.0.0a3', 'grpcio>=1.20.0', 'grpcio-tools>=1.20.0'],
    python_requires='>=3',
    license='BSD License',
    url='https://github.com/caminerinc/treelab-pySDK',
    long_description='The Treelab Python API provides an easy way to integrate Treelab with any external system. The API closely follows REST semantics, uses JSON to encode objects, and relies on standard HTTP codes to signal operation outcomes.'
)

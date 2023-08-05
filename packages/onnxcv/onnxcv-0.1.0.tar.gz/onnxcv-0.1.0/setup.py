import os
from setuptools import setup, find_packages

with open("requirements.txt", "r") as req:
    req = req.read().splitlines()

path = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(path, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='onnxcv',
    version='0.1.0',
    author="Ayaz Amin",
    packages=find_packages('onnxcv'),
    install_requires=req,
    description="An ONNX inference engine for computer vision",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/ChromoBacterium/OnnxCV"
)
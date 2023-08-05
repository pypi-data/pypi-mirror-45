import os

from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "dhttp",
    version = read('version.txt'),
    author = "Gustavo Rehermann",
    author_email = "rehermann6046@gmail.com",
    description = ("A simple, dynamic, decorator-based HTTP server inspired by Node.js's Express. Supports trio, TLS and WebSockets."),
    license = "MIT",
    keywords = "http server httpd express decorator simple easy dynamic trio tls ssl websocket websockets",
    packages=['dhttp'],
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=read('requirements.txt').split('\n'),
    classifiers=[
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "License :: OSI Approved :: MIT License",
    ],
)
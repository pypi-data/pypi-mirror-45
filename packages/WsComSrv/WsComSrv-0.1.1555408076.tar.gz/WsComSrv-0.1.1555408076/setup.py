import setuptools

setup = dict(
    name="WsComSrv",
    version="0.1",
    author="Julian Kimmig",
    author_email="julian-kimmig@gmx.net",
    description="A basic websocket communication server",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/JulianKimmig/websocket_communication_server",
    packages=setuptools.find_packages(),
    install_requires=['FilterDict','websocket-client','websockets'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)

if __name__ == "__main__":
    setuptools.setup(**setup)

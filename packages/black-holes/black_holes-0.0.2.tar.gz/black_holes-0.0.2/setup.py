import setuptools
import pathlib

HERE = pathlib.Path(__file__).parent

README = (HERE / 'README.md').read_text()
REQUIREMENTS = (HERE / 'requirements.txt').read_text()

setuptools.setup(
    name='black_holes',
    version='0.0.2',
    author="Jose A. Salgado",
    author_email="jose.salgado.wrk@gmail.com",
    description="Secrets handle lib.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/JoseSalgado1024/black-holes",
    packages=['black_holes'],
    install_requires=REQUIREMENTS,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)

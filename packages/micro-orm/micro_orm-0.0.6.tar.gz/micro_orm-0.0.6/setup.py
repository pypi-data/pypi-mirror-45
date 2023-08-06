import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='micro_orm',
    version='0.0.6',
    author='Royner Chavarría',
    author_email='roynercharo@hotmail.com',
    description='A small orm for database uses, based on django ORM',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/RooYnnER/micro-orm',
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['pymysql'],
    python_requires=">=3.5"
)

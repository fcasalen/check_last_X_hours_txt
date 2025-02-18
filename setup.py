from setuptools import setup, find_packages

setup(
    name='check_last_x_hours_txt',
    version='0.1.0',
    license="GNU General Public License",
    author="fcasalen",
    author_email="fcasalen@gmail.com",
    description="check if a datetime string in a txt file is in the last X horas, to control scripts runs",
    packages=find_packages(),
    include_package_data=True,
    install_requires=open('requirements.txt').readlines(),
    long_description=open("README.md").read(),
    classifiers=[
        "Development Status :: 5 - Prodution/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12"
    ]
)

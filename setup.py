from setuptools import setup, find_packages

setup(
    name="structured_simulation",
    version="0.1.0",
    packages=find_packages(),  # 查找所有包

    package_data={
        'structured_simulation': ['*.pyd'],   # including all .pyd
    },
    include_package_data=True,  # including all .pyd
    install_requires=[
        "numpy",  # dependencies
        "pandas",
        "sqlalchemy",
        "seaborn"
    ],
)

from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='AllenTools',
    version='0.1.0',
    description='个人工具',
    author='Allen Shen',
    author_email='932142511@qq.com',
    url='https://github.com/AlllenShen/AllenTools',
    packages=['allentools'],
    install_requires=required,
    zip_safe=False,
    include_package_data = True
)
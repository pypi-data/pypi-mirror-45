from setuptools import setup, find_packages

setup(
    name="cfn-deployer",
    version="0.4",
    py_modules=['cfndeployer', 'cfn'],
    packages=find_packages(),
    author="Cory Kitchens",
    author_email="corykitchens@gmail.com",
    long_description="cfndeployer allows the automation of deploying CloudFormation Stacks",
    install_requires=[
        "Click",
        "boto3"
    ],
    entry_points='''
        [console_scripts]
        cfn-deployer=cfndeployer:main
    ''',
)
import click
from cfn import CfnDeploy

@click.command()
def main():
  with open('.cfndeployrc') as f:
    config = f.read()
    cfn_deploy = CfnDeploy()
    cfn_deploy.deploy_stacks()


if __name__=="__main__":
  main()
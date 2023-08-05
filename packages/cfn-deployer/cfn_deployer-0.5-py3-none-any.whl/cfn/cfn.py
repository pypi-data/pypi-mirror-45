import sys
import json
import botocore
import boto3
import os
from botocore.exceptions import ClientError

cache = {}

class CfnObject:
  def read_file(self, file):
    with open(file) as f:
      return f.read()

  def read_json(self, json_file):
    if '.json' in json_file or 'cfndeployrc' in json_file:
      data = self.read_file(json_file)
      return json.loads(data)
    else:
      print(json_file)
      return json.loads(json_file)
  
  def read_yaml(self, yaml_file):
    try:
      return open(yaml_file).read()
    except Exception as e:
      raise(e)

class CfnDeploy(CfnObject):
  def __init__(self, config='./.cfndeployrc'):
    self.stacks = []
    self.config = self.read_json(config)

  def generate_stacks(self):
    for stack in self.config['Stacks']:
      current_stack = CfnStack(**stack)
      self.stacks.append(current_stack)
  
  def deploy_stacks(self):
    if not len(self.stacks):
      self.generate_stacks()
    for stack in self.stacks:
      stack.deploy()

class CfnTemplate(CfnObject):
  def __init__(self, template):
    self.__template = self.read_yaml(template)
  
  def get_template(self):
    return self.__template

class CfnParameters(CfnObject):
  def __init__(self, params):
    self.params = self.read_json(params)

  def __getitem__(self, k):
    if k in self.params.keys():
      return self.params[k]
    else:
      return []
  
  def add(self, k, v):
    param = {'ParameterKey': k, 'ParameterValue': v}
    self.params['Parameters'].append(param)

class CfnStack(object):
  def __init__(self, stack_name, template_body, parameters=None, assumed_role=None, profile=None, outputs=None, imports=None):
    self.__stack_name = stack_name
    self.__template_body = CfnTemplate(template_body)
    
    if parameters is not None:
      self.__params = CfnParameters(parameters)
    else:
      self.__params = parameters
    self.__assumed_role = assumed_role
    self.__outputs = outputs
    self.__imports = imports
    self.__profile = profile

  def exists(self):
    try:
      resp = self.__client.describe_stacks(StackName=self.__stack_name)
      return self.__stack_name == resp['Stacks'][0]['StackName']
    except Exception as e:
      print('{} does not exist'.format(self.__stack_name))
      return False
  
  def to_request_params(self):
    request_params = {}
    request_params['StackName'] = self.__stack_name
    request_params['TemplateBody'] = self.__template_body.get_template()
    if self.__params is not None:
      request_params['Parameters'] = self.__params['Parameters'] or None
      request_params['Capabilities'] = self.__params['Capabilities'] or None
      request_params['Tags'] = self.__params['Tags'] or None
    return request_params
  def create(self):
    try:
      request_params = self.to_request_params()
      res = self.__client.create_stack(**request_params)
      return 'StackId' in res
    except Exception as e:
      print(e)

  def update(self):
    try:
      request_params = self.to_request_params()
      print(request_params)
      res = self.__client.update_stack(**request_params)
      return 'StackId' in res
    except ClientError as e:
      print(f"Error updated stack -> {self.__stack_name}")
      print(e)

  def wait_for_event(self, event_name):
    waiter = self.__client.get_waiter(event_name)
    print('Waiting for {} to achieve status of {}'.format(self.__stack_name, event_name))
    try:
      waiter.wait(StackName=self.__stack_name)
      print('{} completed'.format(event_name))
    except botocore.exceptions.WaiterError as e:
      print('{} received the error {}'.format(event_name, e))
  
  def check_for_outputs(self):
    if self.__outputs:
      resp = self.__client.describe_stacks(StackName=self.__stack_name)
      stack = resp['Stacks'][0]
      if 'Outputs' in stack and len(stack['Outputs']):
        for output in stack['Outputs']:
          if self.__outputs == output['OutputKey']:
            cache[self.__outputs] = output
  
  def check_for_imports(self):
    if not self.__imports:
      return
    if self.__imports in cache.keys():
      self.__params.add(self.__imports, cache[self.__imports]['OutputValue'])

  def deploy(self):
    if self.__profile is not None:
      print('Setting profile')
      session = boto3.Session(profile_name=self.__profile)
      self.__client = session.client('cloudformation')
    else:
      self.__client = boto3.client('cloudformation')
    self.check_for_imports()
    if self.exists():
      print(f'{self.__stack_name} exists. Attempting to UPDATE')
      if self.update():
        self.wait_for_event('stack_update_complete')
    else:
      print(f'{self.__stack_name} does not exist. Attempting to CREATE')
      if self.create():
        self.wait_for_event('stack_create_complete')
    self.check_for_outputs()
    print(cache)

if __name__=="__main__":

  cfn_deploy = CfnDeploy()
  cfn_deploy.deploy()
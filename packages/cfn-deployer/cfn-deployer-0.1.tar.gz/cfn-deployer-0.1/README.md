# cfn-deploy
Automate the deploying of CloudFormation Stacks.

## Installation
```
$ pip install cfn-deploy
```

## Usage
```
$ cfn-deploy
```

## Pre-Reqs
Create a `.cfndeployrc` file in the project directory. This file contains the following JSON schema

### .cfndeployrc Schema

#### Stacks
`Stacks` contains a list of CloudFormation Stacks to deploy. 

### Stack
A `Stack` contains the required keys `stack_name`, `template_body` with the optional keys
- `parameters`
- `capabilities`
- `tags`
- `profile`

### Example .cfndeployrc file
```
{
	"Stacks": [{
		"stack_name": "HelloWorld",
		"template_body": "mystack.yaml"
		"parameters": "path/to/my/params.json",
		"profile": "my_aws_profile"	
	}]
}
```
### TODOs
- Test coverage
- Logging
- Accept S3 endpoints for Templates
- Accept JSON files for Templates
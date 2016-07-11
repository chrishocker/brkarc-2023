# BRKARC-2023 Automation Samples

## Prerequisites

### Install Ansible
```
yum -y install libffi-devel openssl-devel
pip install git+git://github.com/ansible/ansible.git@stable-2.1
```

### Install EC2 Clients
```
pip install awscli
```

### Configure EC2 Credentials

### Create secrets.yml file

Place this into the main repository directory. This is going to include items that you do not want to be visible in the ansible playbooks. This may include items such as the IOS SSH user count, a path to the ec2-user SSH keyfile that was used when the CSR was launched, or a smart license token.


## Using the CSR CloudFormation Template
CloudFormation templates can be launched via the AWS web console or the AWS CLI. Ansible also has a CloudFormation module that can be used.

The following example creates a new CloudFormation stack using the AWS CLI and the csr-cf-template.json file in this repository. It will launch a CSR into an existing VPC subnet and assign an already configured security group.

```
aws cloudformation create-stack --stack-name chrisstack 
--template-body file://///Users/chocker/Code/brkarc-2023/csr-cf-template.json 
--parameters 
ParameterKey=PrivateIpAddress,ParameterValue="172.24.0.100" 
ParameterKey=VpcId,ParameterValue="vpc-7cb4cf19"
ParameterKey=SecurityGroupId,ParameterValue="sg-332c9257"
ParameterKey=SubnetId,ParameterValue="subnet-35a3d66c"
```

To see the status of the CloudFormation stack, use the describe-stacks command.

```
aws cloudformation describe-stacks --stack-name chrisstack
```

To delete the CloudFormation stack, use the delete-stack command.

```
aws cloudformation delete-stack --stack-name chrisstack
```

Note that an inital CSR configuration can be applied by using the user data option in the CloudFormation template. Generally, this would be used for items such as creating IOS user accounts or modifying the intial configuration of interfaces.

## Using the Ansible Playbooks
The easiest playbook to get started with the "Network Exec Command". This will validate the Ansible installation and AWS API permissions. Since you would be running this against an already existing CSR, you will need to manually configure the Ansible inventory file. The inventory file is set in the ansible.cfg file, and is currenlty set as the "hosts" file in the main repository directory.

*Note: You can limit the scope of any ansible playbook by using the --limit option.*

### Launch a CSR into an existing VPC
This playbook will create a new CSR with a single interface. You will need to modify the Ansible variables at the top of the playbook for your environment.

The playbook configures the CSR for an IAM role in preparation for an HA configuration. You can delete this item if it is not needed. If it is needed, you will need to create the IAM role before running this playbook.

```
ansible-playbook aws-create-csr.yml --extra-vars "hostname=tenant1_csr_a private_ip=172.24.0.254"
```

Two items are passed as extra Ansible variables. The first is the hostname that will be used for the EC2 Name key. The second is the private IP address that will be used by the CSR. This should be an used IP address of the subnet in which the CSR is launched.

### Enable Smart Licensing
You will need a smart license account with demo or valid CSR licenses for this to work. You can include the smart license directly into the playbook or in the secrets.yml file.

```
ansible-playbook aws-sl.yml --limit tenant1_csr_a
```

### Configure AWS High Availability
This playbook uses the EC2 APIs to gather the data needed to configure AWS HA on the CSR. You should have already created the ReplaceRouteRole IAM role and assigned to the CSR when it was created. You will need the AWS CLI tools installed, and AWS access permissions enabled.

```
ansible-playbook aws-ha.yml
```
### Network Exec Commands
You can use this playbook to run exec commands such as 'show version' or 'ping 8.8.8.8' to multiple CSRs. 

```
ansible-playbook ios-cli.yml -e "command='show version'"
```

Note the use of double quotes to encapulate the Ansible variable and single quotes inside the double quotes to encapsulate the IOS exec command.

### Delete the AWS CSR
This sample playbook will check for a smart license and return it to the smart license pool. It will then delete the CSR from AWS and remove it from the Ansible inventory file.

```
ansible-playbook aws-delete-csr.yml --limit tenant1_csr_a
```



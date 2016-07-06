Prereqs
- Create secrets.yml
- Create idtoken.yml

Launch a CSR
ansible-playbook create-csr.yml --extra-vars "hostname=tenant1-csr-a private_ip=172.24.0.254"

Enable Smart License
ansible-playbook aws-sl.yml --limit tenant1-csr-a

aws cloudformation create-stack --stack-name chrisstack --template-body file://///Users/chocker/Code/brkarc-2023/csr-cf-template.json \
--parameters ParameterKey=PrivateIpAddress,ParameterValue="172.24.0.100" \
ParameterKey=VpcId,ParameterValue="vpc-7cb4cf19" \
ParameterKey=SecurityGroupId,ParameterValue="sg-332c9257" \
ParameterKey=SubnetId,ParameterValue="subnet-35a3d66c"

aws cloudformation describe-stacks --stack-name chrisstack
aws cloudformation delete-stack --stack-name chrisstack



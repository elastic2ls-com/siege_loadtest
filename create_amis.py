#This scrript only needs to be ran whenever amazon AMI's need to be created or changed.
#Once the AMI's are created, they will be reused until removed or updated.
import subprocess

def execute_cmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    return p.communicate() 

regions = {
    'eu-central-1': 'ami-487d4d55',
    'ap-northeast-1': 'ami-decfc0df',
    'sa-east-1': 'ami-cb04b4d6',
    'ap-southeast-2': 'ami-d1e981eb',
    'ap-southeast-1': 'ami-83406fd1',
    'us-east-1': 'ami-705d3d18',
    'us-west-2': 'ami-4dd4857d',
    'us-west-1': 'ami-17fae852',
    'eu-west-1': 'ami-783a840f'
}


## create launch configs
for region in regions:
    print regions[region]

    # create security group
    cmd = [
        'aws',
        'ec2',
        'create-security-group',
        '--group-name', 'coreos-siege',
        '--description', 'Load testing',
        '--region', region 
    ]
    resp = execute_cmd(cmd)
    print resp
    
    # configure security group
    cmd = [
        'aws',
        'ec2',
        'authorize-security-group-ingress',
        '--group-name',
        'coreos-siege',
        '--protocol', 'tcp',
        '--port',
        '22',
        '--cidr',
        '0.0.0.0/0',
        '--region', region 
    ]
    resp = execute_cmd(cmd)

    # create launch configs
    # The followint key is not valid. Please replace the key with your valid ssh key. This is a random example I randomly smashed into my keyboard.
    user_data = """#cloud-config

ssh_authorized_keys:
- ssh-rsa REPLACE_ME  --> 2EAAAABIwAAAa.sjdkfja/sdfjasdjfsadj/fjadisjicjnnqqQ6LnMhAdo+8JbBa5o3VaJ2VULhsn6MW18ADgqwerTNxr2c6QZ+Xis8q0HEMZlUN1dirrtonYGOkQasidfklsadnfnvASNunasifuDN== <username>@something.net"""
    print("Generating micro configs for %s" % region)
    cmd = [
        'aws',
        'autoscaling',
        'create-launch-configuration',
        '--launch-configuration-name', 'coreos-siege-micro',
        '--image-id', regions[region],
        '--instance-type', 't2.micro',
        '--region', region,
        '--security-groups', 'coreos-siege',
        '--user-data', user_data
    ]
    resp = execute_cmd(cmd)
    print resp

    print("Generating medium configs for %s" % region)
    cmd = [
        'aws',
        'autoscaling',
        'create-launch-configuration',
        '--launch-configuration-name', 'coreos-siege-medium',
        '--image-id', regions[region],
        '--instance-type', 't2.medium',
        '--region', region,
        '--security-groups', 'coreos-siege',
        '--user-data', user_data
    ]
    resp = execute_cmd(cmd)
    print resp

    print("Generating large configs for %s" % region)
    cmd = [
        'aws',
        'autoscaling',
        'create-launch-configuration',
        '--launch-configuration-name', 'coreos-siege-large',
        '--image-id', regions[region],
        '--instance-type', 'm3.xlarge',
        '--region', region,
        '--security-groups', 'coreos-siege',
        '--user-data', user_data
    ]
    resp = execute_cmd(cmd)
    print resp

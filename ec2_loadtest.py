from fabric.api import run, env, parallel, get
from fabric.tasks import execute
import json
import subprocess
import os
from time import sleep
import socket
import sys

env.user = "core"
#REPLACE ME: replace the ssh key with your path and key name.
env.key_filename = "~/.ssh/<YOUR_KEY>"
env.timeout = 60
env.connection_attempts = 3
env.warn_only = True
env.disable_known_hosts = True

def pull_latest():
    run('echo "pulling latest images"')
    run('docker pull jcostello84/siege-loadtest:latest')

def start_latest(domain, login_url, url_list, etc_hosts, concurrent, reps, time, use_login):
    run('echo "starting latest images"')
    cmd = [
        'docker run -it',
        '-e DOMAIN="%s"' % domain,
        '-e LOGIN_URL="%s"' % login_url,
        '-e URL_LIST="%s"' % url_list,
        '-e ETC_HOSTS="%s"' % etc_hosts,
        '-e USE_LOGIN="%s"' % use_login
    ]
    if time != "NOT_SET" and time != None:
        cmd.append('jcostello84/siege-loadtest:latest -v -c%s -t%s' % (concurrent, time))
    else:
        cmd.append('jcostello84/siege-loadtest:latest -v -c%s -r%s' % (concurrent, reps))

    cmd.append('| sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]//g" | tee ~/siege_%s.log' % env.host_string)
    run(' '.join(cmd))
    get('~/siege_%s.log' % env.host_string, './')
    

@parallel
def deploy(domain, login_url, url_list, etc_hosts, concurrent, reps, time, use_login):
    pull_latest()
    start_latest(domain, login_url, url_list, etc_hosts, concurrent, reps ,time, use_login)

def get_avail_zone(region):
    cmd = [
        'aws',
        'ec2',
        'describe-availability-zones',
        '--region', region
    ]
    resp = execute_cmd(cmd)
    json_data = json.loads(resp[0])
    return json_data['AvailabilityZones'][0]['ZoneName']

def execute_cmd(cmd):
    print("Executing cmd: %s" % cmd)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    return p.communicate() 

def main(group_name, config_name, domain, login_url, url_list, etc_hosts, concurrent, reps, time, use_login, tries, num_instances, region):

    ## create group
    cmd = [
        'aws',
        'autoscaling',
        'create-auto-scaling-group',
        '--auto-scaling-group-name', group_name,
        '--launch-configuration-name', config_name,
        '--min-size', num_instances,
        '--max-size', num_instances,
        '--desired-capacity', num_instances,
        '--availability-zones', '%s' % get_avail_zone(region),
        '--region', region 
    ]
    resp = execute_cmd(cmd)

    retries = 0
    group_status = json.loads(os.popen('aws autoscaling describe-auto-scaling-groups --auto-scaling-group-name %s --region %s' % (group_name, region)).read())
    while retries < 10:
        retries += 1
        print group_status
        if len(group_status['AutoScalingGroups']) > 0:
            if "Status" in group_status['AutoScalingGroups'][0].keys():
                if tries < 10:
                    # If there is a delete in progress, increment tries by 1, and call this function
                    # recursively(have to do this otherwise group does not get created)
                    tries += 1
                    print("Delete in progress!! Waiting 10 seconds and trying again.")
                    sleep(10);
                    main(group_name, config_name, domain, login_url, url_list, etc_hosts, concurrent, reps, time, use_login, tries, num_instances, region)
                    return
                else:
                    print("Failed to start scaling group. A previous delete may be in progress. Aborting")
                    return
            if len(group_status['AutoScalingGroups'][0]['Instances']) > 0:
                print("Scaling group ready")
                break
        else:
            print("Waiting for auto scaling group to start")
        sleep(10)
        group_status = json.loads(os.popen('aws autoscaling describe-auto-scaling-groups --auto-scaling-group-name %s --region %s' % (group_name, region)).read())

    # get instance IDs
    cmd = ['aws', 'autoscaling', 'describe-auto-scaling-groups', '--auto-scaling-group-names', group_name, '--region', region]
    resp = execute_cmd(cmd)

    json_data = json.loads(resp[0])
    instances = {} 
    instances_arg = ""
    for group in json_data['AutoScalingGroups']:
        for instance in group['Instances']:
            instances[instance['InstanceId']] = {}

    # get public IP addresses
    cmd = ['aws', 'ec2', 'describe-instances', '--region', region, '--instance-ids', '"%s"' % '" "'.join(instances.keys())]
    resp = os.popen(' '.join(cmd)).read()
    json_data = json.loads(resp)

    for reservation in json_data['Reservations']:
        for instance in reservation['Instances']:
            instances[instance['InstanceId']]['public_ip'] = instance['PublicIpAddress']

    hosts = []
    for instance in instances:
        hosts.append(instances[instance]['public_ip'])

    execute(deploy, domain=domain, login_url=login_url, url_list=url_list, etc_hosts=etc_hosts, concurrent=concurrent, reps=reps, time=time, use_login=use_login, hosts=hosts)

if __name__ == "__main__":


    domain = sys.argv[1]
    use_login = sys.argv[2]
    login_url = sys.argv[3]
    url_list = sys.argv[4]
    etc_hosts = sys.argv[5]
    concurrent = sys.argv[6]
    reps = sys.argv[7]
    config_name = "coreos-siege-%s" % sys.argv[8]
    num_instances = sys.argv[9]
    group_name = sys.argv[10]
    region = sys.argv[11]
    #region = "us-west-2" # other regions don't work yet

    # time is optional
    time = None
    if len(sys.argv) > 12:
        time = sys.argv[12]

    tries = 0
    main(group_name, config_name, domain, login_url, url_list, etc_hosts, concurrent, reps, time, use_login, tries, num_instances, region)

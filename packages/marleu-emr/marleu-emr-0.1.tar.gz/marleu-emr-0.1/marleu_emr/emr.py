import argparse
import requests
import paramiko
import credstash
import boto3
import time

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

DEFAULT_REGION = "eu-central-1"
YARN_PORT = 8088
SSH_PORT = 22
CREDSTASH_STORE_SUFFIX = 'credential-store'
CHECK_CANCEL_RETRIES = 15
CHECK_CANCEL_DURATION_SEC = 10


# TODO add pagination for list_steps (for now at least this script will fail if we have too many pending steps)

def __get_master_dns(cluster_id, region):
    client = boto3.client('emr', region_name=region)
    cluster = client.describe_cluster(ClusterId=cluster_id)
    master_dns = cluster['Cluster']['MasterPublicDnsName']
    print('Found master dns name: {}'.format(master_dns))
    return master_dns


def __get_running_apps_ids(master_dns):
    running_apps_uri = 'http://{}:{}/ws/v1/cluster/apps/?state=running'.format(master_dns, YARN_PORT)
    # TODO handle errors?
    get_apps_response = requests.get(running_apps_uri).json()["apps"]
    if get_apps_response is not None:
        ids = map(lambda x: x["id"], get_apps_response["app"])
        return list(ids)
    else:
        return []


def __list_steps(region, cluster_id, states):
    client = boto3.client('emr', region_name=region)
    return client.list_steps(
        ClusterId=cluster_id,
        StepStates=states
    )


def __wait_for_step_cancelation(cluster_id, region, retries):
    while __list_steps(region, cluster_id, ['CANCEL_PENDING', 'PENDING'])['Steps']:
        print('Waiting for the steps to be canceled..')
        time.sleep(CHECK_CANCEL_DURATION_SEC)
        if retries is 0:
            raise Exception('Pending steps still not canceled!!')
        else:
            __wait_for_step_cancelation(cluster_id, region, retries - 1)


def cancel_pending_steps(cluster_id, region):
    print('Killing pending steps for cluster {} in region {}...'.format(cluster_id, region))
    steps = __list_steps(region, cluster_id, ['PENDING'])
    step_ids = list(map(lambda x: x['Id'], steps['Steps']))
    client = boto3.client('emr', region_name=region)
    print('Canceling pending steps: {}'.format(step_ids))
    if step_ids:
        client.cancel_steps(
            ClusterId=cluster_id,
            StepIds=step_ids
        )
        __wait_for_step_cancelation(cluster_id, region, CHECK_CANCEL_RETRIES)


def __getSshKey(env, region, key_pair_credstash_key):
    credstash_store = '{}-{}'.format(env, CREDSTASH_STORE_SUFFIX)
    return credstash.getSecret(name=key_pair_credstash_key, table=credstash_store, region=region)


def __exec_command_through_ssh(master_dns, ssh_key_pair, command):
    pkey = paramiko.RSAKey.from_private_key(StringIO(ssh_key_pair))
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(master_dns, username='hadoop', port=SSH_PORT, pkey=pkey)
    stdin, stdout, stderr = client.exec_command(command)
    stderr_string = stderr.read().decode("utf-8")
    if stderr_string:
        error_message = 'Error executing ssh command: {}'.format(stderr_string)
        client.close()
        raise Exception(error_message)
    stdout_string = stdout.read().decode("utf-8")
    if stdout_string:
        return stdout_string


def __kill_yarn_app(id, env, region, master_dns, key_pair_credstash_key):
    ssh_key_pair = __getSshKey(env, region, key_pair_credstash_key)
    kill_command = 'yarn application -kill {}'.format(id)
    try:
        print(__exec_command_through_ssh(master_dns, ssh_key_pair, kill_command))
    except Exception as err:
        if 'Killed application' not in str(err):
            raise err


def kill_running_apps(env, region, cluster_id, key_pair_credstash_key):
    print('Killing running apps for cluster {} in region {}...'.format(cluster_id, region))
    master_dns = __get_master_dns(cluster_id, region)
    running_app_ids = __get_running_apps_ids(master_dns)
    for id in running_app_ids:
        print('Killing app with id: {}'.format(id))
        __kill_yarn_app(id, env, region, master_dns, key_pair_credstash_key)


def run_on_master_node(command, env, region, cluster_id, key_pair_credstash_key):
    master_dns = __get_master_dns(cluster_id, region)
    ssh_key_pair = __getSshKey(env, region, key_pair_credstash_key)
    print(__exec_command_through_ssh(master_dns, ssh_key_pair, command))


def __add_env_credstash_args(action_parser):
    action_parser.add_argument("-k", "--key-pair-credstash-key", default=None, required=True,
                               help="credstash key in which is located the key-pair "
                                    "to SSH the master node. Needed to kill running steps.")
    action_parser.add_argument("-e", "--env", default=None, required=True, help="environment.")


def get_parser():
    """get the parsers dict"""
    parsers = {'super': argparse.ArgumentParser(description="Emr utility collection")}

    parsers['super'].add_argument("-r", "--region", default=DEFAULT_REGION,
                                  help="pass a region or it will be used the default one:" + DEFAULT_REGION)

    parsers['super'].add_argument("-c", "--cluster-id", default=None, required=True,
                                  help="cluster id")

    subparsers = parsers['super'].add_subparsers(help='Try "emr command --help"')

    action = 'cancel-pending-steps'
    parsers[action] = subparsers.add_parser(action, help="cancel all the pending emr steps")
    parsers[action].set_defaults(action=action)

    action = 'kill-running-apps'
    parsers[action] = subparsers.add_parser(action, help="kill all the running emr applications")
    parsers[action].set_defaults(action=action)
    __add_env_credstash_args(parsers[action])

    action = 'cancel-steps-kill-apps'
    parsers[action] = subparsers.add_parser(action, help="cancel all the pending emr steps and then "
                                                         "kill all the running emr applications")
    parsers[action].set_defaults(action=action)
    __add_env_credstash_args(parsers[action])

    action = 'run-on-master-node'
    parsers[action] = subparsers.add_parser(action, help="run a command on the emr master node through SSH")
    parsers[action].set_defaults(action=action)
    __add_env_credstash_args(parsers[action])
    parsers[action].add_argument("-x", "--command", default=None, required=True,
                                 help="command to execute on master node "
                                      "through SSH connection")

    return parsers


def main():
    parsers = get_parser()
    args = parsers['super'].parse_args()

    region = args.region
    cluster_id = args.cluster_id

    if "action" in vars(args):
        if args.action == "cancel-pending-steps":
            cancel_pending_steps(cluster_id, region)
            return
        if args.action == "kill-running-apps":
            key_pair_credstash_key = args.key_pair_credstash_key
            env = args.env
            kill_running_apps(env, region, cluster_id, key_pair_credstash_key)
            return
        if args.action == "cancel-steps-kill-apps":
            key_pair_credstash_key = args.key_pair_credstash_key
            env = args.env
            cancel_pending_steps(cluster_id, region)
            kill_running_apps(env, region, cluster_id, key_pair_credstash_key)
            return
        if args.action == "run-on-master-node":
            key_pair_credstash_key = args.key_pair_credstash_key
            env = args.env
            command = args.command
            run_on_master_node(command, env, region, cluster_id, key_pair_credstash_key)
    else:
        parsers['super'].print_help()


if __name__ == '__main__':
    main()

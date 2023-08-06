import os
import urllib3
import yaml
import json
from time import sleep
from subprocess import Popen, PIPE, STDOUT
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from .storage import default_bucket, key_prefix, source_dir_tar_file_name
from .utils import file_system_protocol, is_gke_provider


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
default_job_name = 'dcp'
default_namespace = 'default'
config.load_kube_config()


def _get_job_command(job_name, entry_file_location):
    path = '{0}/{1}/{2}'.format(
        key_prefix,
        job_name,
        source_dir_tar_file_name)
    src = '{protocol}{bucket}/{path}'.format(
        protocol=file_system_protocol(),
        bucket=default_bucket,
        path=path)
    return 'dcp_run {} {}'.format(
        src, entry_file_location)


def interpolate_body(body, job_name, command, gpu_count):
    body['metadata']['name'] = job_name
    spec = body['spec']['template']['spec']
    containers = spec['containers']
    container = containers[0]
    container['command'] = ['/bin/sh', '-c', command]
    container['name'] = job_name
    if gpu_count > 0:
        container['resources']['limits']['nvidia.com/gpu'] = gpu_count
    body['spec']['template']['spec']['containers'][0] = container
    return body


def _get_tf_job_yaml_file_path(gpu_count):
    suffix = 'gke' if is_gke_provider() else 'dke'
    suffix = 'tpu' if suffix == 'gke' and gpu_count == 0 else suffix
    filename = 'tf_job_yaml/tf_job_{}.yaml'.format(suffix)
    return os.path.join(os.path.dirname(__file__), filename)


def _api_body(job_name, entry_file_location, gpu_count):
    file_path = _get_tf_job_yaml_file_path(gpu_count)
    with open(file_path) as f:
        job_template = yaml.safe_load(f)
    command = _get_job_command(job_name, entry_file_location)
    return interpolate_body(body=job_template,
                            command=command,
                            job_name=job_name,
                            gpu_count=gpu_count)


def create_job(job_name, entry_file_location, gpu_count):
    body = _api_body(job_name, entry_file_location, gpu_count)
    try:
        api_instance = client.BatchV1Api()
        api_instance.create_namespaced_job(
            "default", body, pretty=True)
        print('job {} is created'.format(job_name))
    except ApiException as e:
        print(e)


def _get_ready_state_pod(job_name):
    api_instance = client.CoreV1Api()
    try:
        res = api_instance.list_namespaced_pod(
            default_namespace,
            include_uninitialized=True,
            label_selector='job-name={}'.format(job_name))
        pod = res.items.pop()
        pod_name = pod.metadata.name
        for condition in pod.status.conditions:
            if condition.type == 'Ready':
                return pod_name
        return None

    except ApiException as e:
        print(e)


def _pod_log(name):
    api_instance = client.CoreV1Api()
    try:
        res = api_instance.read_namespaced_pod_log(
            name,
            default_namespace,
            follow=True,
            pretty=True,
            timestamps=True)
        print(res)
    except ApiException as e:
        print(e)


def get_log(job_name):
    try:
        ready_state_pod = None
        while not ready_state_pod:
            ready_state_pod = _get_ready_state_pod(job_name)
            print('.', end=' ')
            sleep(1)
        _pod_log(ready_state_pod)

    except ApiException as e:
        print(e)

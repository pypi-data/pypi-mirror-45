import os
from kubernetes import client, config


def is_gke_provider():
    kube_config_default_location = os.environ.get(
        'KUBECONFIG', '{}/.kube/config'.format(os.environ['HOME']))
    _, active_context = config.list_kube_config_contexts(
        kube_config_default_location)
    return active_context['name'].startswith('gke')


def file_system_protocol():
    return 'gs://' if is_gke_provider() else 's3://'

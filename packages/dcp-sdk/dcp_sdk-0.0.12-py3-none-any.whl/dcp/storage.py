import os
import tarfile
import tempfile
import tensorflow as tf
from .utils import file_system_protocol


key_prefix = 'source'
default_bucket = 'dcp-bucket'
source_dir_tar_file_name = 'sourcedir.tar.gz'
default_namespace = 'default'


def _dst(job_name):
    return '{protocol}{bucket}/{key_prefix}/{job_name}/{source_file}'.format(
        protocol=file_system_protocol(),
        bucket=default_bucket,
        key_prefix=key_prefix,
        job_name=job_name,
        source_file=source_dir_tar_file_name)


def tar_and_upload(source_files, job_name):
    with tempfile.NamedTemporaryFile(delete=True) as f:
        with tarfile.open(mode='w:gz', fileobj=f) as t:
            t.add(source_files, recursive=True)
        f.seek(0)
        src = f.name
        dst = _dst(job_name=job_name)
        tf.gfile.Copy(src, dst)
    print('source code is uploaded to {}'.format(dst))


def get_source_files(entry_file, source_dir):
    if not source_dir:
        return entry_file
    return source_dir

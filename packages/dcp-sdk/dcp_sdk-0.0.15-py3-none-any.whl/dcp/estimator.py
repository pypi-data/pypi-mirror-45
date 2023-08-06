import os
import random
from time import localtime, strftime
from os.path import exists, isdir
from dcp.storage import get_source_files, tar_and_upload
from dcp.job import create_job, default_job_name, get_log


class Estimator:
    def __init__(self, entry_file, gpu_count, source_dir=None):
        exists(entry_file)
        if source_dir:
            isdir(source_dir)
        self.source_dir = source_dir
        self.entry_file = entry_file
        self.gpu_count = gpu_count

    def get_random_job_name(self, job_name):
        return '{0}-{1}-{2}'.format(job_name if job_name else default_job_name,
                                    strftime("%Y-%m-%d-%H-%M-%S", localtime()),
                                    random.randint(100, 999))

    def upload_source_files(self, job_name):
        source_files = get_source_files(self.entry_file, self.source_dir)
        tar_and_upload(source_files, job_name)

    def _entry_location(self, entry_file, source_dir):
        if not source_dir:
            return entry_file
        return os.path.join(source_dir, entry_file)

    def _get_entry_location(self, entry_file, source_dir):
        location = self._entry_location(entry_file, source_dir)
        if os.path.isabs(location):
            return location[1:]
        return location

    def fit(self, job_name=None):
        job_name = self.get_random_job_name(job_name)
        self.upload_source_files(job_name)
        entry_file_location = self._get_entry_location(
            entry_file=self.entry_file, source_dir=self.source_dir)
        create_job(job_name=job_name,
                   gpu_count=self.gpu_count,
                   entry_file_location=entry_file_location)
        # get_log(job_name)

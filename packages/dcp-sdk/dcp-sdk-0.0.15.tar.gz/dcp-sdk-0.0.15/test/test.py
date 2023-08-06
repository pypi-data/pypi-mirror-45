# from dcp.estimator import Estimator
from dcp.storage import tar_and_upload
from dcp.job import create_job
from dcp.estimator import Estimator
import os


def test_fit_without_source_dir_entry_file():
    entry_file = os.path.join(
        os.path.dirname(__file__),
        'iris/source_dir/entry_file.py')
    estimator = Estimator(entry_file=entry_file, gpu_count=1)
    estimator.fit()


def get_real_path(path):
    return os.path.join(os.path.dirname(__file__), path)


def test_fit_with_source_dir():
    entry_file = 'main.py'
    source_dir = get_real_path('imagenet/source_dir')
    estimator = Estimator(entry_file=entry_file,
                          source_dir=source_dir,
                          gpu_count=1)
    estimator.fit()


def test_tpu_keras():
    entry_file = 'resnet50.py'
    source_dir = get_real_path('tpu/resnet50_keras')
    estimator = Estimator(entry_file=entry_file,
                          source_dir=source_dir,
                          gpu_count=0)
    estimator.fit()


# test_fit_without_source_dir_entry_file()
test_fit_with_source_dir()
# test_tpu_keras()

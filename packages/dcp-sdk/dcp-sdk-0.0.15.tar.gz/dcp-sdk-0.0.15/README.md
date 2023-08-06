# dcp sdk
sdk for machine learning in dudaji cloud k8s gpu cluster

## Install
```bash
$ pip install dcp-sdk
```

## env variables
```
AWS_ACCESS_KEY_ID=ID
AWS_SECRET_ACCESS_KEY=PW
S3_ENDPOINT=minio.du.io
S3_USE_HTTPS=0
S3_VERIFY_SSL=0
TF_CPP_MIN_LOG_LEVEL=3
```

## sample
examples  
├── hello.py  
└── sample.py

hello.py
```python
print("hello dcp sdk")
```

sample.py
```python
import os
from dcp.estimator import Estimator


def main():
    entry_file = os.path.join(
        os.path.dirname(__file__),
        'hello.py')
    estimator = Estimator(entry_file=entry_file, gpu_count=1)
    estimator.fit()

```

```shell
python sample.py
```





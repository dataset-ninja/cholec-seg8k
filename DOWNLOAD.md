Dataset **CholecSeg8k** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/o/g/hb/T3TFPWjLh2h8JOAB9WjVIakAdtixLpLxNEyj8w8A3gxT8WBpaT7u1i2FukGMHFBTypxowA958SO3vxq1CWxyhBIpGBGMbzNd5eWYUiMuSu6pqgGrXser8nwzwvAz.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='CholecSeg8k', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://www.kaggle.com/datasets/newslab/cholecseg8k/download?datasetVersionNumber=11).
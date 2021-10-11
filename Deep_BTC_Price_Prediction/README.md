# Docker Jupyter
In order to have a jupyter notebook with preinstalled tensorflow you can simplu use this command:
```shell
docker run -it --name <YOUR-IMAGE-NAME> -p 8888:8888 -v ${PWD}:/tf/notebooks tensorflow/tensorflow:latest-py3-jupyter
```
## Description
Our code is largely notebook based. 
Main points are as follows:
- fMRI/behavioural dynamic connectivity matrix
- Connectivity Gradients

![](https://github.com/miki998/connectivity_gradient_analysis/master/media/readme_plots)


## Requirements

Our requirements are listed in `build/requirements.txt`


* Unix is supported, but we mostly used Mac OS.
* 64-bit Python 3.8 is the version we use (or later version can be used).
* CUDA toolkit 11.1 or later.
* Python libraries: see [requirements.txt](./build/requirements.txt) for exact library dependencies. You can use the following
  commands with Miniconda3 to create and activate your `brain` Python environment:
    - `cd ./build/`
    - `conda create -n "brain" python=3.8.13`
    - `conda activate brain`
    - `<PATH TO YOUR CONDA PYTHON EXEC> python -m pip install requirements.txt`

* Docker users:
    - Ensure you have correctly installed
      the [NVIDIA container runtime](https://docs.docker.com/config/containers/resource_constraints/#gpu).
    - Use the [None for now](./Dockerfile) to build an image with the required library dependencies.

## Getting started

Open jupyter notebooks inside the `notebooks` folder (not yet added)

```
jupyter notebook "NOTEBOOK-NAME"
```

## NOTICE
1/

2/

3/

## Acknowledgement

We borrow a lot from these repositories:

**BrainSpace

```
https://github.com/MICA-MNI/BrainSpace
```



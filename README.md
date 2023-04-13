# Bachelor Thesis Codebase

This is the codebase that we used to explore whether data augmentation approaches can improve the out-of-domain performance of query-based meeting summarisation models. 

This codebase uses the dataset provided by [QMSUM](https://arxiv.org/pdf/2104.05938.pdf), and the [DYLE](https://arxiv.org/pdf/2110.08168.pdf) model.

## Folder organisation and contributions
We conducted our research by using DYLE's repository, in which they provided these following files and folders:
- dataloaders: the python scripts to convert original dataset to the uniform format.
- oracle: Scripts to generate extractive oracles
- utils: Various utility functions, such as cleaning and rouge
- Experiment.py: Main file for our model
- config.py: Set model configuration
- Modules: Contains implementation of our dynamic extraction module
- test.py: Run test set
- train.py: Train the model

After updating the code they provided and adapting it for our research purposes, we were able to explore various data augmentation approaches. Note that we only kept the code that was used to produce our final results and visualisations, and didn't include all the intermediate experiments to keep a clear folder structure. The ```dataAugmentation``` folder contains the code used to produce the augmented data, and the ```visualisations``` folder contains the code and Jupyter notebooks used to produce the final visualisations used in our paper, along with the actual figures that were used.

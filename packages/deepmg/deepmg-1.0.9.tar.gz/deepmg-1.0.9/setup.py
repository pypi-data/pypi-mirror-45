import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deepmg",
    version="1.0.9",
    author="Thanh-Hai Nguyen",
    author_email="hainguyen579@gmail.com",
    description="A python package to visualize/train/predict data using machine/deep learning algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.integromics.fr/published/deepmg",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

#what's NEW ###
# version: 0.4.5: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + fix name log of vgg, cnn model (with padding)
# + rename "ab" --> "spb"
# + set up to use all available gpus cudaid < -1

# version: 0.4.6: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + fix folder in creating images for whole dataset

# version: 0.4.7: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + add gpu_memory_fraction to control memory of gpu required used, to be able to run multiple jobs using gpu
#      The second method is the gpu_memory_fraction option, 
#      which determines the fraction of the overall amount of memory that each visible GPU should be allocated
#      if gpu_memory_fraction = 0: attempts to allocate only as much GPU memory based on runtime allocations: 
#               it starts out allocating very little memory, and as Sessions get run and more GPU memory is needed, 
#               we extend the GPU memory region needed by the TensorFlow process
# + cudaid : <-1: use cpu, -1: use all available gpus, >-1: use specific gpu 

# version: 0.4.8: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + cudaid : <-2: use cpu; -2: use cpu if there is no available gpu; -1: use all available gpus; >-1: use specific gpu 

# version: 0.4.9: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + change ab -> spb in vis_data.py

# version: 0.4.10: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + fix error of external validation, check whether #features equal between internal and external
# + include external evaluation into training whole dataset when set ext_test = y
# + scaler_section function: use temporary var to store max_v_temp instead of options.min_v = np.min(train_x) will affect the followed experiment (for external,...)

# version: 0.4.11: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + fix error of predict, commenting "os.remove(prefix_file_log+"_mean_auc.txt") --> not found to remove" in predict
# + readme : add "pip install keras_sequential_ascii", correct some directions on use of parameters
# + add check library of keras_sequential_ascii in check_ok option to check whether package work properly
# 

# version: 0.4.12: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + fix error of predict on external validation of fc on 1D data, add "v_data = np.reshape(v_data, (v_data.shape[0], 1, v_data.shape[1]))"
# + add additional function to collect results into a file to plot with all folds, 
#       and other function such as deleting unncesary files, summarize results...
# + fix: error 
#           pkg_resources.VersionConflict: 
#               (bleach 1.5.0 (/anaconda2/lib/python2.7/site-packages), Requirement.parse('bleach>=2.1.0'))
#    --> pip install --upgrade bleach

# version: 0.4.13: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + error: "Message: trial mode expires in 30 days" --> upgrade conda and python
#       conda update python
#       conda update conda
#      


# version: 0.4.14: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + error: LICENSE  in setup.py --> License
#       readme.md --> README.md

# version: 0.4.15: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + save models and load models for predicting in machine learning with SVM and RF

# version: 0.5.0: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + finish functional with repeat experiment with config file: 
#       added, modified get_default_value,para_config_file,string_to_numeric,write_para,validation_para
# + select para from cmd other than config file
# + add mode of config (type_run='config'): only creating config file
# + move naming_log_final to experiment.py
# + move textcolor_display to utils.py

# version: 0.5.1: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + update readme with -h

# version: 0.5.2: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + update setup.py url to "https://git.integromics.fr/published/deepmg"
# + add model: Gradient Boosting Trees: gbt

# version: 0.5.3: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + clean header of files
# + comment code
# + experiment.py: set --padding to "y" as default
# + experiment.py: add "tn, fp, fn, tp," to save to *_eachfold.txt and *_sum.txt in header and content of file *_eachfold.txt and *_sum.txt
# + read_results.py (important!): combine results

# version: 0.5.4: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + read_results.py: just need to specify a name for output, remove list of files after done
# + experiment.py: 
#     ++ fixed the issue of auc_score in external validation evaluation: forgot to divide v_data with coefficient 
#     ++ add score loss, confusion matrix to external evaluation
#     ++ fix error read result in classic lm : replace '--' to '++'

# version: 0.5.5: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + read_results.py: add try-catch if file is empty

# version: 0.5.6: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + read_results.py: add information #files summarized

# version: 0.5.7: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + experiment.py: fix issue with "if  options.scale_mode ['minmaxscaler' , 'mms'] :"   

# version: 0.5.8: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + readme: update paper, code jupiter

# version: 0.5.9: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + experiment.py: create global map for fills each fold

# version: 0.5.10: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + refresh

# version: 0.5.11: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + experiment.py: modify mcc to run for a large number of sample

# version: 0.5.13: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + experiment.py: modify mcc to run for a large number of sample
# + experiment.py: add validation to model
# + experiment.py: add comments to guide how to use n_fold (option k)
# + experiment.py: set save_rf to 'y' as default value
# + __main__: set up to run only once with training on training set and predicting on test set.
# 

# version: 0.5.14: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + experiment.py: add parameter "save_labels" to control saving labels to log --> save running time for big data


# version: 0.5.15: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + experiment.py: correct error with infinitive for svm, rf

# version: 0.5.15: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + experiment.py and models_def: add parameter rf_max_depth for random forest

# version: 0.5.21: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + experiment.py and models_def: add parameter rf_max_depth for gbc_model

# version: 0.5.22: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + Readme: update paper and information of the package

# version: 0.5.23: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + experiment: add para time_whole_run to set the time of run for whole set

# version: 0.5.23: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + experiment: add para rf_max_features in decision Trees


# version: 0.5.24: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + experiment: add sound when finished, add para --sound_fini

# version: 0.5.29: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + experiment: set default value that no weight will be saved (improve speed and memory)

# version: 0.5.30: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + experiment: move sound_fini to the end of code

# version: 0.5.31: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + experiment: change the requirement of patten name of external from "*_zx.csv" to "*z_x.csv" so that it is easier to test on external set standalone

# version: 0.5.32: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + experiment: set up so that if using scaling but not using binning, then creating the folder rathan raw

# version: 0.5.33: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + experiment: rename pretrained for model trained read from weight file

# version: 0.5.34: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + experiment: note to do not add extension in command

# version: 0.5.37: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + experiment: predict_proba
# + experiment: add an option to collect result details
# + experiment: add an option 'ext_data' to use a different name for external set than original name of training+test set
# + experiment: set --time_run=1 in default
# + experiment: name for ext_data in log
# + naming log consistently
# + issues with collecting loss+acc of each epoch


# version: 1.0.0: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + convert to python3, you need to install some packages in python 3 as followings:
#python3 -m pip install numpy
#python3 -m pip install matplotlib
#python3 -m pip install ConfigParser
#python3 -m pip install pandas
#python3 -m pip install sklearn
#python3 -m pip install tensorflow
#python3 -m pip install keras
#python3 -m pip install keras_sequential_ascii
# + fixed issue with save_d
# + changed options: time_run --> run_time, time_whole_run --> whole_run_time
# + increase decimal places to 8 in results in _eachfold.text

# version: 1.0.6: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + add notification python3 to setup and readme
# + moved "if __name__ == "__main__":  " to the first part of __main__.py


# version: 1.0.7 and 8: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + changed 'import experiment' to 'from deepmg import experiment' to fix 'ModuleNotFoundError: No module named....'

# version: 1.0.9: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# + add emb_data zfill, zfills

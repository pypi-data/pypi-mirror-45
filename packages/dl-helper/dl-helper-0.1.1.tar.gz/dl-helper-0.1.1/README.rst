dl-helper
=========

A (small) Python package that contains a number of miscellaneous utility
classes and functions to ease the work of developing Deep Learning models,
especially when working on Jupyter Notebooks.

Contains:

* ``console_capture``, a module to provide objects that allow capturing
  stdout/stderr for later replay.
  Intended for IPython notebooks, in which if we close the browser window 
  with a running kernel all subsequent console output is lost
* ``krs.krs_model_io``: helpers to save/load DL models developed in Keras
* ``krs.krs_utils``: miscellaneous helpers for Keras models (print out graphs
  of a Keras model, compare two models, improve/fix Keras progress bars).


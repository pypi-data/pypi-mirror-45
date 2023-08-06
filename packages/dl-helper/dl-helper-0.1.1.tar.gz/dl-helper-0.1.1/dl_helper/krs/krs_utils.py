'''
Some small utilities for Keras model creation & training

Paulo Villegas, 2017-2019
'''

from __future__ import division, print_function
import numpy as np


from keras.utils.vis_utils import model_to_dot
from IPython.core.display import SVG


# ----------------------------------------------------------------------


def model_layers_graph(model, show_shapes=True):
    '''
    Display a Keras model in a notebook by rendering it as SVG
    '''
    dot = model_to_dot(model, show_shapes=show_shapes)
    #dot.set( 'rankdir', 'LR')
    for n in dot.get_nodes():
        n.set('style', 'filled')
        n.set('fillcolor', 'aliceblue')
        n.set('fontsize', '10')
        n.set('fontname', 'Trebuchet MS, Tahoma, Verdana, Arial, Helvetica, sans-serif')
    img = dot.create_svg()
    return SVG(data=img)


def model_layers_list(model):
    '''
    List all layers in a Keras model
    '''
    print("Model layers:")
    for i, layer in enumerate(model.layers):
        print("  {:3}: {}".format(i+1, layer.name))
        #print ("      ",layer.trainable_weights,layer.non_trainable_weights)
        for n, w in zip(layer.trainable_weights, layer.get_weights()):
            print("       {}: w = {}".format(n, w.shape))


# ----------------------------------------------------------------------

def pred_show(pred, truth=None):
    '''
    Show prediction results
    '''
    print('  n res ' if truth is None else '  n res true    ', end='     ')
    for c in range(pred.shape[1]):
        print("{:7}".format(c+1), end=' ')
    for i, r in enumerate(pred):
        print('\n{:3}  {:2}'.format(i+1, np.argmax(r)+1), end=' ')
        if truth is not None:
            print("{:4}".format(truth[i]+1), end=' ')
            print("ok" if truth[i] == np.argmax(r) else "- ", end=" ")
        print(' -> ', end=' ')
        for c in r:
            print("{:7.5f}".format(c), end=' ')
    print()


# ----------------------------------------------------------------------

def model_compare(m1, m2):
    '''
    Compare the weights in two models (the two models are assumed to have the
    same architecture)
    '''
    print("Comparing weights in model layers:")
    i = 0
    for l1, l2 in zip(m1.layers, m2.layers):
        print("  {:3}: {}".format(i+1, l1.name.encode('utf8')))
        assert(l1.name == l2.name)
        #print ("      ",layer.trainable_weights,layer.non_trainable_weights)
        for w1, w2 in zip(l1.get_weights(), l2.get_weights()):
            if not np.allclose(w1, w2):
                print('Not equal')
                for c1, c2 in zip(w1, w2):
                    print(c1, c2)
                return
        i += 1


# ----------------------------------------------------------------------

def wrapper_decorator(orig_update):
    """
    A decorator for the progress bar update function, so that it does
    not crash on I/O errors (assumedly due to some multithreading collision
    in ipykernel, patched in https://github.com/ipython/ipykernel/pull/123
    for ipykernel > 4.3.1)
    """
    def wrapped_update(self, current, values=[], **kwargs):
        try:
            orig_update(self, current, values, **kwargs)
        except ValueError:
            pass

    return wrapped_update


def wrapper_init(orig):
    """
    A decorator for the progress bar constructor, to increase the update interval
    to 1 sec (and thus reduce the amount of information generated)
    """
    def wrapped_init(self, target, **kwargs):
        kwargs['interval'] = 1
        orig(self, target, **kwargs)

    return wrapped_init


# Monkey-patch the constructor in the Progbar class to use 1-sec update intervals
import keras.utils.generic_utils as kgutils
kgutils.Progbar.__init__ = wrapper_init(kgutils.Progbar.__init__)

#kgutils.Progbar.update = wrapper_decorator(kgutils.Progbar.update)


# ----------------------------------------------------------------------

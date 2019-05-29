"""
.. _tut_kim_sw:

Train a Stillinger-Weber potential
==================================

In this tutorial, we train a Stillinger-Weber (SW) potential for silicon that is archived
on OpenKIM_.
"""


##########################################################################################
# Before getting started to train the SW model, let's first install the SW # model::
#
#    $ kim-api-collections-management install user SW_StillingerWeber_1985_Si__MO_405512056662_005
#
# .. seealso::
#    This installs the model and its driver into the ``User Collection``. See
#    :ref:`install_model` for more information about installing KIM models.
#
# We are going to create potentials for diamond silicon, and fit the potentials to a
# training set of energies and forces consisting of compressed and stretched diamond
# silicon structures, as well as configurations drawn from molecular dynamics trajectories
# at different temperatures.
# Download the training set :download:`Si_training_set.tar.gz
# <https://raw.githubusercontent.com/mjwen/kliff/pytorch/examples/Si_training_set.tar.gz>`
# and extract the tarball: ``$ tar xzf Si_training_set.tar.gz``. The data is stored in
# **extended xyz** format, and see :ref:`doc.dataset` for more information of this format.
#
# .. warning::
#    The ``Si_training_set`` is just a toy data set for the purpose to demonstrate how to
#    use KLIFF to train potentials. It should not be used to train any potential for real
#    simulations.
#
# Let's first import the modules that will be used in this example.

from kliff.models import KIM
from kliff.loss import Loss
from kliff.calculator import Calculator
from kliff.dataset import Dataset


##########################################################################################
# Model
# -----
#
# We first create a KIM model for the SW potential, and print out all the available
# parameters that can be optimized (we call this ``model parameters``).

model = KIM(model_name='SW_StillingerWeber_1985_Si__MO_405512056662_005')
model.echo_model_params()


##########################################################################################
# The output is generated by the last line, and it tells us the ``name``, ``value``,
# ``size``, ``data type`` and a ``description`` of each parameter.
#
# .. note::
#    You can provide a ``path`` argument to the method ``echo_model_params(path)`` to
#    write the available parameters information to a file indicated by ``path``.
#
# .. note::
#    The available parameters information can also by obtained using the **kliff**
#    :ref:`cmdlntool`:
#    ``$ kliff model --echo-params SW_StillingerWeber_1985_Si__MO_405512056662_005``
#
# Now that we know what parameters are available for fitting, we can optimize all or a
# subset of them to reproduce the training set.

model.set_fitting_params(
    A=[[5.0, 1.0, 20]], B=[['default']], sigma=[[2.0951, 'fix']], gamma=[[1.5]]
)
model.echo_fitting_params()


##########################################################################################
# Here, we tell KLIFF to fit four parameters ``B``, ``gamma``, ``sigma``, and ``A`` of the
# SW model. The information for each fitting parameter should be provided as a list of
# list, where the size of the outer list should be equal to the ``size`` of the parameter
# given by ``model.echo_model_params()``. For each inner list, you can provide either one,
# two, or three items.
#
# - One item. You can use a numerical value (e.g. ``gamma``) to provide an initial guess
#   of the parameter. Alternatively, the string ``'default'`` can be provided to use the
#   default value in the model (e.g. ``B``).
#
# - Two items. The first item should be a numerical value and the second item should be
#   the string ``'fix'`` (e.g. ``sigma``), which tells KLIFF to use the value for the
#   parameter, but do not optimize it.
#
# - Three items. The first item can be a numerical value or the string ``'default'``,
#   having the same meanings as the one item case. In the second and third items, you can
#   list the lower and upper bounds for the parameters, respectively. A bound could be
#   provided as a numerical values or ``None``. The latter indicates no bound is applied.
#
# The call of ``model.echo_fitting_params()`` prints out the fitting parameters that we
# require KLIFF to optimize. The number ``1`` after the name of each parameter indicates
# the size of the parameter.
#
# .. note::
#    The parameters that are not included as a fitting parameter are fixed to the default
#    values in the model during the optimization.
#
#
# Training set
# ------------
#
# KLIFF has a :class:`~kliff.dataset.Dataset` to deal with the training data (and possibly
# test data). For the silicon training set, we can read and process the files by:

dataset_name = 'Si_training_set'
tset = Dataset()
tset.read(dataset_name)
configs = tset.get_configs()


##########################################################################################
# The ``configs`` in the last line is a list of :class:`~kliff.dataset.Configuration`.
# Each configuration is an internal representation of a processed **extended xyz** file,
# hosting the species, coordinates, energy, forces, and other related information of a
# system of atoms.
#
#
# Calculator
# ----------
#
# :class:`~kliff.calculator.Calculator` is the central agent that exchanges information
# and orchestrate the operation of the fitting process. It calls the model to compute the
# energy and forces and provide this information to the `Loss function`_ (discussed below)
# to compute the loss. It also grabs the parameters from the optimizer and update the
# parameters stored in the model so that the up-to-date parameters are used the next time
# the model is evaluated to compute the energy and forces. The calculator can be created
# by:

calc = Calculator(model)
calc.create(configs)


##########################################################################################
# where ``calc.create(configs)`` does some initializations for each each
# configuration in the training set, such as creating the neighbor list.
#
#
# Loss function
# -------------
#
# KLIFF uses a loss function to quantify the difference between the training set data and
# potential predictions and uses minimization algorithms to reduce the loss as much as
# possible. KLIFF provides a large number of minimization algorithms by interacting with
# SciPy_. For physics-motivated potentials, any algorithm listed on
# `scipy.optimize.minimize`_ and `scipy.optimize.least_squares`_ can be used. In the
# following code snippet, we create a loss of energy and forces, where the residual
# function uses an ``energy_weight`` of ``1.0`` and a ``forces_weight`` of ``0.1``, and
# ``2`` processors will be used to calculate the loss. The ``L-BFGS-B`` minimization
# algorithm is applied to minimize the loss, and the minimization is allowed to run for a
# a max number of 100 iterations.

steps = 100
residual_data = {'energy_weight': 1.0, 'forces_weight': 0.1}
loss = Loss(calc, residual_data=residual_data, nprocs=2)
loss.minimize(method='L-BFGS-B', options={'disp': True, 'maxiter': steps})


##########################################################################################
# The minimization stops after running for 27 steps.  After the minimization, we'd better
# save the model, which can be loaded later for the purpose to do a retraining or
# evaluations. If satisfied with the fitted model, you can also write it as a KIM model
# that can be used with LAMMPS_, GULP_, ASE_, etc. via the kim-api_.

model.echo_fitting_params()
model.save('kliff_model.pkl')
model.write_kim_model()


##########################################################################################
# The first line of the above code generates the output.  A comparison with the original
# parameters before carrying out the minimization shows that we recover the original
# parameters quite reasonably. The second line saves the fitted model to a file named
# ``kliff_model.pkl`` on the disk, and the third line writes out a KIM potential named
# ``SW_StillingerWeber_1985_Si__MO_405512056662_005_kliff_trained``.
#
# .. seealso::
#    For information about how to load a saved model, see :ref:`doc.modules`.
#
#
# .. _OpenKIM: https://openkim.org
# .. _SciPy: https://scipy.org
# .. _scipy.optimize.minimize: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html
# .. _scipy.optimize.least_squares: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html
# .. _kim-api: https://openkim.org/kim-api/
# .. _LAMMPS: https://lammps.sandia.gov
# .. _GULP: http://gulp.curtin.edu.au/gulp/
# .. _ASE: https://wiki.fysik.dtu.dk/ase/

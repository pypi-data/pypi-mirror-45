# # -*- coding: utf-8 -*-
# """
# Created on 06.04.19 by ibaris
# """
# from __future__ import division
#
# import numpy as np
#
# from rspy.units.ancillary import Units
# from rspy.units.auxiliary import Zero
#
#
# class Quantity(np.ndarray):
#     """ Physical Quantities
#
#     This module defines the `Quantity` objects. A Quantity object represents a number with some an associated unit.
#
#     Attributes
#     ----------
#     Quantity.value : np.ndarray
#         The numerical value of this quantity in the units given by unit.
#     Quantity.unit : sympy.physics.units.quantities.Quantity
#         An object that represents the unit associated with the input value.
#     Quantity.dtype : type
#         The data type of the value
#     Quantity.copy: bool
#         The entered copy bool value.
#     Quantity.order : str
#         Order of the array.
#     Quantity.subok : bool
#         The entered subok value.
#     Quantity.ndmin : int
#         Minimum number of dimensions
#     Quantity.name : str
#         Name of the Quantity
#     Quantity.constant : bool
#         Information about if the Quantity is an constant or not.
#     Quantity.unitstr : str
#         Parameter unit as str.
#     Quantity.unit_mathstr : str
#         Parameter unit as math text.
#     Quantity.label : str
#         Parameter name and unit as math text.
#     Quantity.expr : np.ndarray
#         The whole expression (value * unit) as sympy.core.mul.Mul.
#     Quantity.tolist : list
#         Value and unit as a list.
#
#     Methods
#     -------
#     decompose()
#         Return value as np.ndarray and unit as sympy.physics.units.quantities.Quantity object.
#     decompose_expr(expr)
#         Extract value and unit from a sympy.core.mul.Mul object.
#     set_name(name)
#         Set a name for the current Quantity.
#     convert_to(unit, inplace=True)
#         Convert unit to another units.
#     set_constant(bool)
#         Set a `Quantity` object as constant. In this case, every operation will drop the name of the Quantity.
#     Raises
#     ------
#     UnitError
#     DimensionError
#
#     See Also
#     --------
#     respry.units.Units
#
#     """
#
#     def __new__(cls, value, unit=None, dtype=None, copy=True, order=None,
#                 subok=False, ndmin=0, name=None, constant=True, verbose=False):
#         """
#         The Quantity object is meant to represent a value that has some unit associated with the number.
#
#         Parameters
#         ----------
#         value : float, int, numpy.ndarray, sympy.core.all_classes
#             The numerical value of this quantity in the units given by unit.
#
#         unit : sympy.physics.units.quantities.Quantity, str
#             An object that represents the unit associated with the input value.
#             Must be an `sympy.physics.units.quantities.Quantity` object or a string parsable by
#             the :mod:`~respy.units` package.
#
#         dtype : numpy.dtype, type, int, float, double, optional
#             The dtype of the resulting Numpy array or scalar that will
#             hold the value.  If not provided, it is determined from the input,
#             except that any input that cannot represent float (integer and bool)
#             is converted to float.
#
#         copy : bool, optional
#             If `True` (default), then the value is copied.  Otherwise, a copy will
#             only be made if ``__array__`` returns a copy, if value is a nested
#             sequence, or if a copy is needed to satisfy an explicitly given
#             ``dtype``.  (The `False` option is intended mostly for internal use,
#             to speed up initialization where a copy is known to have been made.
#             Use with care.)
#
#         order : {'C', 'F', 'A'}, optional
#             Specify the order of the array.  As in `~numpy.array`.  This parameter
#             is ignored if the input is a `Quantity` and ``copy=False``.
#
#         subok : bool, optional
#             If `False` (default), the returned array will be forced to be a
#             `Quantity`.
#
#         ndmin : int, optional
#             Specifies the minimum number of dimensions that the resulting array
#             should have.  Ones will be pre-pended to the shape as needed to meet
#             this requirement.  This parameter is ignored if the input is a
#             `Quantity` and ``copy=False``.
#         name : str
#             A name for the created Quantity.
#         constant : bool
#             If True and the constant has a name the name will be replaced after a operation.
#
#         """
#
#         x = np.array(value, dtype=dtype, copy=copy, order=order, subok=subok, ndmin=ndmin)
#         x = np.atleast_1d(x)
#
#         if x.dtype == int:
#             dtype = np.double
#             x = x.astype(dtype)
#         else:
#             pass
#
#         obj = x.view(type=cls)
#
#         if unit is None:
#             obj.unit = Zero
#         else:
#             obj.unit = Units.get_unit(unit)
#
#         obj.__dimension = obj.unit.dimension
#
#         obj.value = x
#
#         if name is None:
#             obj.name = b''
#         else:
#             obj.name = name
#
#         obj.constant = constant
#         obj.dtype = dtype
#         obj.copy = copy
#         obj.order = order
#         obj.subok = subok
#         obj.ndmin = ndmin
#         obj.__quantity__ = True
#         obj.verbose = verbose
#
#         return obj
#
#     # --------------------------------------------------------------------------------------------------------
#     # Magic Methods
#     # --------------------------------------------------------------------------------------------------------
#     def __repr__(self):
#         prefix = '<{0} '.format(self.__class__.__name__)
#         sep = ', '
#         arrstr = np.array2string(self,
#                                  separator=sep,
#                                  prefix=prefix)
#
#         if self.name is None or self.name is b'':
#             return '{0}{1} [{2}]>'.format(prefix, arrstr, Units.unit2str(self.unit))
#
#         else:
#             return '{0}{1} {2} in [{3}]>'.format(prefix, arrstr, self.name, Units.unit2str(self.unit))
#
#     def __array_finalize__(self, obj):
#         if obj is None:
#             return
#         else:
#             self.value = getattr(obj, 'value', None)
#             self.unit = getattr(obj, 'unit', None)
#             self.name = getattr(obj, 'name', None)
#             self.constant = getattr(obj, 'constant', None)
#             self.copy = getattr(obj, 'copy', None)
#             self.order = getattr(obj, 'order', None)
#             self.subok = getattr(obj, 'subok', None)
#             self.ndmin = getattr(obj, 'ndmin', None)
#             self.dimension = getattr(obj, 'dimension', None)
#             self.__quantity__ = getattr(obj, '__quantity__', None)
#             self.verbose = getattr(obj, 'verbose', None)
#
#     def __getitem__(self, item):
#         value = super(Quantity, self).__getitem__(item)
#
#         return self.__new_instance(value, self.unit)
#
#     # --------------------------------------------------------------------------------------------------------
#     # Properties
#     # --------------------------------------------------------------------------------------------------------
#
#     # --------------------------------------------------------------------------------------------------------
#     # Private Methods
#     # --------------------------------------------------------------------------------------------------------
#     def __setattr(self, value, unit, dtype, copy, order, subok, ndmin, name, constant, verbose):
#
#         self.value = value
#         self.dtype = dtype
#         self.copy = copy
#         self.order = order
#         self.subok = subok
#         self.ndmin = ndmin
#         self.name = name
#         self.constant = constant
#         self.verbose = verbose
#         self.unit = unit
#         self.dimension = unit.dimension
#
#     def __new_instance(self, value, unit=None, dtype=None, copy=True, order=None, subok=None, ndmin=None, name=None,
#                        constant=None, verbose=None):
#         quantity_subclass = self.__class__
#
#         unit = self.unit if unit is None else unit
#         dtype = self.dtype if dtype is None else dtype
#         copy = self.copy if copy is None else copy
#         order = self.order if order is None else order
#         subok = self.subok if subok is None else subok
#         ndmin = self.ndmin if ndmin is None else ndmin
#
#         if name is None:
#             name = None if self.constant else self.name
#
#         constant = self.constant if constant is None else constant
#         verbose = self.verbose if verbose is None else verbose
#
#         array = np.array(value, dtype=dtype, copy=copy, order=order, ndmin=ndmin)
#         array = np.atleast_1d(array)
#
#         view = array.view(quantity_subclass)
#         view.__setattr(array, unit, dtype, copy, order, subok, ndmin, name, constant, verbose)
#         view.__array_finalize__(view)
#
#         if subok:
#             return view.value
#
#         return view
#
# # a = np.zeros((3, 2))
# #
# # q = Quantity([1, 2, 3, 4, 5], 'm', name='pipi', subok=True)
# # b = q[0:3]
# #
# # q = Quantity(a.transpose(), 'm', name='pipi', subok=True)


#    QASDAD, the quick and simple data analysis and documentation program
#    Copyright (C) 2018 Volker Weißmann . Contact: volker.weissmann@gmx.de

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

##If DEBUG is set to True, QASDAP will print
DEBUG=False
##If PROFILE is set to True, QASDAP will print the time for needed for various tasks
PROFILE=True

import time
#@cond INTERNAL
startTimeMillis = int(round(time.time() * 1000))
#@endcond INTERNAL
##Returns milliseconds since program startup
def millis():
	return int(round(time.time() * 1000))-startTimeMillis
if PROFILE:
	print("python.py started")

import sympy
from sympy import symbols
import sympy.physics
from sympy.physics.units import meter, second, hertz, kilogram, coulomb, volt, ampere, ohm, henry, kelvin, newton, joule, siemens, farad, watt
import numpy as np
import scipy.optimize
import math
import io #used in readFile
import os #used in Plot.showHere
#from enum import Enum
import matplotlib
import matplotlib.pyplot #as plt
#from process_latex import process_sympy #TODO: this might require https://pypi.org/project/documentparser/

if PROFILE:
	print(str(millis()) + " ms for importing")

#    QASDAD, the quick and simple data analysis and documentation program
#    Copyright (C) 2018 Volker Weißmann . Contact: volker.weissmann@gmx.de

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

SPEED_OF_LIGHT = 299792458*meter/second
MAGNETIC_CONSTANT = 4*sympy.pi*10**-7*newton*ampere**-2
ELECTRIC_CONSTANT = 1/(4*sympy.pi*10**-7*newton*ampere**-2*299792458**2*meter**2*second**-2)
PLANCK_CONSTANT= 6.626070040*10**-34*joule*second
HBAR = 1.054571800*10**-34*joule*second
GRAVITATIONAL_CONSTANT = 6.67408*10**-11*meter**3*kilogram**-1*second**-2
ELEMENTARY_CHARGE = 1.6021766208*10**-19*coulomb
FINE_STRUCTURE_CONSTANT = 0.0072973525664

good_known_units_short = {
	"m": meter,
	"s": second,
	"Hz": hertz,
	"kg": kilogram,
	"C": coulomb,
	"V": volt,
	"A": ampere,
	"\Omega": ohm,
	"H": henry,
	"K": kelvin,
	"N": newton,
	"J": joule,
        "S": siemens,
        "W": watt
		    }
good_known_units_long = {
	"meter": meter,
	"second": second,
	"hertz": hertz,
	"kilogram": kilogram,
	"coulomb": coulomb,
	"volt": volt,
	"ampere": ampere,
	"ohm": ohm,
	"henry": henry,
	"kelvin": kelvin,
	"newton": newton,
	"joule": joule,
        "siemens": siemens,
        "watt": watt,
		    }
#    QASDAD, the quick and simple data analysis and documentation program
#    Copyright (C) 2018 Volker Weißmann . Contact: volker.weissmann@gmx.de

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

#! [toBasicSI]
##\snippet this toBasicSI
def toBasicSI(unit):
	return sympy.physics.units.convert_to(unit,[sympy.physics.units.meter,sympy.physics.units.second,sympy.physics.units.kilogram,sympy.physics.units.coulomb,sympy.physics.units.kelvin])
#! [toBasicSI]
#! [subsSIUnitsOne]
##\snippet this subsSIUnitsOne
def subsSIUnitsOne(expr):
	expr = toBasicSI(expr)
	expr = expr.subs(sympy.physics.units.meter,1)
	expr = expr.subs(sympy.physics.units.second,1)
	expr = expr.subs(sympy.physics.units.kilogram,1)
	expr = expr.subs(sympy.physics.units.coulomb,1)
	expr = expr.subs(sympy.physics.units.kelvin,1)
	return expr
#! [subsSIUnitsOne]
##Exception that occurs if qasdad encounters incompatible dimensions, eg. 3*meter+5*second
class IncompDimensions(Exception):
	pass
##Exception that occurs if there is a free symbol in an expression that should not be there
class FreeSymbolException(Exception):
	pass
#@cond INTERNAL
def checkGetUnitBackend(a):
	try:
		float(a)
		return 1
	except:
		pass
        #TODO diese funktion dokumentiern und im source code nach sympy nach schauen welche isinstance befehler da noch fehlern
	if isinstance(a,sympy.add.Add):
		u = checkGetUnitBackend(a.args[0])
		for i in range(1,len(a.args)):
			#print(a.args[i])
			#print(unit(toBasicSI(u))) meter
			#print(checkGetUnit(toBasicSI(u))) meter
			#print(toBasicSI(checkGetUnitBackend(a.args[i])))
			#if unit(toBasicSI(checkGetUnitBackend(a.args[i]))) != unit(toBasicSI(u)):
			if checkGetUnitBackend(toBasicSI(a.args[i])) != checkGetUnitBackend(toBasicSI(u)):
				print("=============================")
				print(toBasicSI(checkGetUnitBackend(a.args[i])))
				print(toBasicSI(u))
				raise IncompDimensions("incompatible dimensionen")
		return u
	elif isinstance(a,sympy.mul.Mul):
		u = 1
		for arg in a.args:
			u *= checkGetUnitBackend(arg)
		return u
	elif isinstance(a, sympy.power.Pow):
		return checkGetUnitBackend(a.args[0])**a.args[1]
	elif (isinstance(a, sympy.sin) or isinstance(a, sympy.asin) or
	      isinstance(a, sympy.cos) or isinstance(a, sympy.acos) or
	      isinstance(a, sympy.tan) or isinstance(a, sympy.atan)):
		if checkGetUnitBackend(a.args[0]) != 1:
			print("incompatible dimension: The following is not dimensionless but should be")
			print(a.args[0])
			exit(1)
		return 1
	elif isinstance(a, sympy.log):
		for arg in a.args:
			checkGetUnitBackend(arg)
		return 1
	elif isinstance(a, sympy.physics.units.quantities.Quantity):
		return a
	elif isinstance(a, sympy.symbol.Symbol):
		raise FreeSymbolException(str(a))
	else:
		raise IncompDimensions("unsup. op")
		print("unsupported operation for checkGetUnitBackend", type(a))
		exit(1)
#@endcond INTERNAL
##Returns the unit of expr. Exits with errorcode 1 if it encounters incompatible dimensions, eg. 3*meter+5*second
def checkGetUnit(expr):
	#print("============================")
	if DEBUG:
		print("\tcheckGetUnit:")
		print("\t\t", expr)
	try:
		u = checkGetUnitBackend(expr)
	except FreeSymbolException as ex:
		print("Fatal Error: Unable to check and get unit of: ")
		print(expr)
		print("Because of the free symbol:")
		print(ex)
		exit(1)
	if DEBUG:
		print("\t\treturns:", u)
	return u
#@cond INTERNAL
def checkGetUnitTest():
	print("testing checkGetUnit...")
	goodPairs = [[7.4*sympy.physics.units.meter, sympy.physics.units.meter],
		     [1.0*sympy.physics.units.meter, sympy.physics.units.meter],
		     [1*sympy.physics.units.meter, sympy.physics.units.meter],
		     [5*sympy.physics.units.meter, sympy.physics.units.meter],
		     [sympy.physics.units.meter, sympy.physics.units.meter],
		     [3*sympy.physics.units.centimeter + sympy.physics.units.meter, sympy.physics.units.meter, sympy.physics.units.centimeter]]
	
	for pair in goodPairs:
		flag = False
		u = checkGetUnit(pair[0])
		for i in range(1, len(pair)):
			if u == pair[i]:
				flag = True
		assert(flag)
	print("...finished testing checkGetUnit")
if DEBUG:
	checkGetUnitTest()
#@endcond INTERNAL
#    QASDAD, the quick and simple data analysis and documentation program
#    Copyright (C) 2018 Volker Weißmann . Contact: volker.weissmann@gmx.de

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

##Holds an equation, consisting of a sympy equation, a latex equation and a dictionary that matches latex representations to sympy symbols
class Equation:
	##equation as a sympy equation
	#Note: You can get the left side of the equation via object.eqSympy.lhs and the right side similar.
	eqSympy = None
	##equation as a latex string
	eqLatex = None
	##dictionary that matches latex representations to sympy symbols.
	#Note: {latexString: sympySymbol} not {sympySymbol: latexString}
	nameDict = None
	##Construct an Equation from a sympy equation and a dictionary that matches latex representations to sympy symbols. Note: THIS IS CURRENTLY BROKEN
	@staticmethod
	def fromSympy(expr, nameDict):
		if PROFILE:
			startTime = millis()
		if isinstance(expr, str):
			expr = strToSympy(expr)
		ret = Equation()
		ret.nameDict = nameDict
		nameDict = dict([[v,k] for k,v in nameDict.items()])
		ret.eqSympy = expr
		#ret.eqLatex = sympy.latex(expr.subs(nameDict))
		ret.eqLatex = anythingExceptNumbersToTex(expr.subs(nameDict))
		if PROFILE:
			print(str(millis()-startTime) + " ms for fromSympy")
		return ret
	##Constructs an Equation from a latex equation, a dictionary that matches latex representations to sympy symbols and a list with problematic latexStrings
	##\param texSyms: The script used to generate sympy expressions from latex is a bit buggy, sometimes a symbol in the sympy output has a wrong name. You can prevent this by giving fromLatex the list texSyms that includes all latex strings that may be a problem. eq. Equation.formLatex("U_a", [], {}") returns symbols("U_{a}"), but Equation.formLatex("U_a", ["U_a"], {}") returns symbols("U_a")
	@staticmethod
	def fromLatex(latex, texSyms, nameDict):
		if PROFILE:
			startTime = millis()
		ret = Equation()
		ret.eqLatex = latex
		latex = latex.replace("\\right", "").replace("\\left","").replace("\\,","")
		#texSyms = getAllLatexSymbols(latex)
		#print(texSyms)
		#exit(1)
		#texSyms = [item for item in texSyms if item not in ["\\frac", "\\sqrt", "\\left", "\\right"] ]
		try:
			ret.eqSympy = process_sympy(latex).subs(symbols("pi"),sympy.pi)
		except Exception as err:
			print("Unable to parse LaTeX code. Either the following code is not valid LaTeX, or there is a bug in latex2Sympy: ")
			print(latex)
			print("The exception is:")
			print(err)
			exit(1)
		for s in texSyms:
			if s != "" and s != "\\pi" and s != str(process_sympy(s)) and process_sympy(s) in ret.eqSympy.free_symbols:
				nameDict[process_sympy(s)] = s
		ret.eqSympy = ret.eqSympy.subs(nameDict)
		ret.eqSympy = ret.eqSympy.subs(nameDict)
		ret.nameDict = nameDict
		if PROFILE:
			print(str(millis()-startTime) + " ms for fromLatex")
		return ret
	@staticmethod
	def fromSympyAndLatex(sympy, latex, nameDict):
		if isinstance(sympy, str):
			sympy = strToSympy(sympy)
		ret = Equation()
		ret.eqSympy = sympy
		ret.eqLatex = latex
		ret.nameDict = nameDict
		return ret
	#! [Equation showHere]
	##\snippet this Equation showHere
	def showHere(self, label):
		tex("\\begin{equation}")
		tex(self.eqLatex)
		tex("\\label{" + label + "}")
		tex("\\end{equation}")
	#! [Equation showHere]
#    QASDAD, the quick and simple data analysis and documentation program
#    Copyright (C) 2018 Volker Weißmann . Contact: volker.weissmann@gmx.de

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
                
##Column is intended to hold a physical property that has different values in different repititions of the same experiment
class Column:
	##The name that is used to address this Column within this Program (mem is short for memory)
	memName = None
	##data is a list that holds the value of the physical property (with a unit)
	#If the length of data is 1, data is often treated similar to a list with a different length, where every single value is the same.
	data = None
	##delta is a list that holds the measuring inaccuracy (with a unit)
	#delta may be None
	#If delta is not None the lengths of data and delta have to be equivalent
	delta = None
	##Read the documention of mathName
	specialTexMathName = None
	##Read the documention of textName
	specialTexTextName = None
	##Read The documention of mathName and textName
	nameType = None
	##analPropUncert sometimes holds a latex-formatted string of a analytic propagation of uncertainty. Show with tex("$"+col.analPropUncert+"$")
	analPropUncert = None
	#! [Column mathName]
	##\snippet this Column mathName
	##\return Symbol of the physical property that should be used in equations
	def mathName(self):
		if self.specialTexMathName is not None:
			return self.specialTexMathName
		if self.nameType == "eq":
			return self.memName
		if self.nameType == "text":
			return "\\mathrm{" + self.memName + "}"
		print("malformed Column")
		exit(1)
	#! [Column mathName]
	#! [Column textName]
	##\snippet this Column textName
	##\return Name of the physical property that should be used in text
	def textName(self):
		if self.specialTexTextName is not None:
			return self.specialTexTextName
		if self.nameType == "text":
			return self.memName
		if self.nameType == "eq":
			return "$" + self.memName + "$"
		print("malformed Column")
		exit(1)
	#! [Column textName]
	##\return Returns True if the physical property is exact
	def isDeltaZero(self):
		if DEBUG:
			print("\tisDeltaZero:")
			print("\t\tself.memName=", self.memName)
		if self.delta is None:
			if DEBUG:
				print("\t\treturn True")
			return True
		for i in self.delta:
			if i != 0:
				if DEBUG:
					print("\t\treturn False")
				return False
		if DEBUG:
			print("\t\treturn True")
		return True
	##\return data in SI units, gets used in plots. The data type is np.ndarray<np.float64>
	def dataForPlot(self):
		startTime3 = millis()
		ret = np.zeros(len(self.data))
		for i in range(len(self.data)):
			ret[i] = np.float64(subsSIUnitsOne(self.data[i]))
			#ret[i] = withoutUnit(self.data[i])
		if PROFILE:
			print(str(millis()-startTime3) + " ms for dataForPlot")
		return ret
	##\return unit of the physical property
	def unit(self):
		for i in range(len(self.data)):
			if self.data[i] != 0:
				return checkGetUnit(self.data[i])
		print("unable to get unit because data[i] is zero for all i")
		exit(0)
	#Constructor:
	#\param memName The name that is used to address this Column within this Program (mem is short for memory).
	#\param nameType Look at the documentation of Column.mathName and Column.textName for explanation.
	#\param data The value of the physical property including its unit. The data type of data has to be "list".
	##Constructor: Checks if data is an instance of the "list"-class and sets member variables according to arguments
	def __init__(self, memName, nameType, data, specialTexMathName=None, specialTexTextName=None, delta=None):#TODO nameType soll ein optionales argument sein, wenn texMathName und texTextName gegeben sind
		if not isinstance(data, list):
			print("bad argument for Column constructor: data is not a list")
			raise ValueError("Bad argument for Column constructor: data is not a list. type(data): " + str(type(data)))
			exit(1)
		self.memName = memName
		self.nameType = nameType
		self.data = data
		self.specialTexMathName = specialTexMathName
		self.specialTexTextName = specialTexTextName
		self.delta = delta
	##Only Used for debug purposes, exact format is not guaranteed to be stable
	def __str__(self):
		ret = "<" + self.memName
		for i  in self.data:
			ret += " " + str(i) #self.format.format(i)
		ret += ">"
		return ret
	##Only Used for debug purposes, exact format is not guaranteed to be stable
	def __repr__(self):
		return str(self)

##Table is a super thin wrapper around python's dict that ensures that self.cols[key].memName == key
class Table:
        #! [table init]
	##\snippet this table init
	def __init__(self, copy=None):
		if copy is None:
			self.cols = {}
		elif isinstance(copy, Table):
			self.cols = copy.cols #shallow copy
			#print("=====================")
			#print(copy.cols)
			#self = copy #TODO #pythonlernen wieso geht das nicht
			#print(self.cols)
			#print("=====================")
		elif isinstance(copy, list):
			self.cols = {} #shallow copy
			for i in copy:
				self.cols[i.memName] = i
		elif isinstance(copy, dict):
			self.cols = copy #shallow copy
		else:
			print("bad arguments for Table.init")
			exit(1) #TODO raise wäre besser
	#! [table init]
	#! [table getitem]
	##\snippet this table getitem
	def __getitem__(self, key):
		return self.cols[key]
	#! [table getitem]
	#! [table setitem]
	##\snippet this table setitem
	def __setitem__(self, key, value):
		if value.memName != key:
			print("key and memName do not match")
			exit(1)
		self.cols[key] = value
	#! [table setitem]
	#! [table add]
	##\snippet this table add
	def add(self, value):#TODO: should we call this method "add" or "set"?
		if isinstance(value, Column):
			self.cols[value.memName] = value
			return
		elif isinstance(value, Table):
			value = list(value.cols.values())
		elif isinstance(value, dict):
			value = list(value.values())
		elif isinstance(value, list):
			pass
		else:
			print("Bad argument type for Table.add")
			exit(1)#TODO: raise would be better than exit, is there a "wrongTypeException" in python?
		for c in value:
			self.cols[c.memName] = c
	#! [table add]
	##\deprecated
	def addFromEq(self, eq):
		print("use of deprecated function add Table.addFromEq, use calcColumn instead")
		exit(1)
		#print(eq.eqSympy)
		#print(str(eq.eqSympy.lhs))
		#if str(eq.eqSympy.lhs) in eq.nameDict:
		#	memName = eq.nameDict[str(eq.eqSympy.lhs)]
		#else:
		#	memName = str(eq.eqSympy.lhs)
		inverseDict = dict([[v,k] for k,v in eq.nameDict.items()])
		self.add(calcColumn(table, eq.eqSympy.rhs, str(eq.eqSympy.lhs), resultNameType="text", resultMathName=str(eq.eqSympy.lhs.subs(inverseDict)) ))
	def checkGetLen(self):#TODO diese Funktion dokumentieren
		length = 1
		for mem in self.cols:
			if length == 1:
				length = len(self.cols[mem].data)
			elif length != len(self.cols[mem].data):
				print("Error in checkGetLen") #TODO raise wäre besser
				exit(1)
		return length
	def removeRows(self, condition): #TODO: Document this function #TODO mit map kann man das besser schreiben
		condition = strToSympy(condition)
		rowNum = 0
		while rowNum < self.checkGetLen():
			cond = condition
			for mem in self.cols:
				cond = cond.subs(mem, self.cols[mem].data[rowNum])
			if cond:
				for mem in self.cols:
					del self.cols[mem].data[rowNum]
					#self.cols[mem].data = np.delete(self.cols[mem].data, rowNum)
			else:
				rowNum += 1
			
#    QASDAD, the quick and simple data analysis and documentation program
#    Copyright (C) 2018 Volker Weißmann . Contact: volker.weissmann@gmx.de

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

def listToString(data):
	if data is None:
		return "None"
	ret = "["
	if len(data) != 0:
		ret += str(data[0])
	for i in range(1, len(data)):
		ret += "," + str(data[i])
	ret += "]"
	return ret
	
##Important Element for class Plot, gets stored in Plot.lines. Consists of physical property that gets shown in the Plot and, optionally, a fitcurve.
class PlotLine:
	##Constructor. 
	##Adds line to plot with self.ax.errorbar(xColumn.dataForPlot(), yColumn.dataForPlot(), xerr=xdelta, yerr=ydelta, **kwargs) or
	##self.ax.errorbar(xColumn.dataForPlot(), yColumn.dataForPlot(), xerr=xdelta, yerr=ydelta, label=yColumn.textName(), **kwargs)
	def __init__(self, ax, logFile, xColumn, yColumn, xerr, yerr, **kwargs):
		self.ax = ax
		self.logFile = logFile
		self.xcol = Column(xColumn.memName, xColumn.nameType, xColumn.data, xColumn.specialTexMathName, xColumn.specialTexTextName, xColumn.delta)#We need a deep copy of xColumn, xColumn.data and xColumn.delta, because we want to remove all nan's from xColumn.data
		self.ycol = Column(yColumn.memName, yColumn.nameType, yColumn.data, yColumn.specialTexMathName, yColumn.specialTexTextName, yColumn.delta)#Aus mir unerklärlichen Gründen ist das eine deep Copy von yColumn.data, also self.ycol.yColumn[0] = 123 verändern nicht yColumn
		#xData = self.xcol.data.copy()
		#yData = self.ycol.data.copy()
		i = 0
		while True:
			if i >= len(self.xcol.data):
				break
			if isnan(self.xcol.data[i]) or isnan(self.ycol.data[i]):
				self.xcol.data = np.delete(self.xcol.data, i)
				self.ycol.data = np.delete(self.ycol.data, i)
				self.xcol.delta = np.delete(self.xcol.delta, i)
				self.ycol.delta = np.delete(self.ycol.delta, i)
			else:
				i += 1
		if xerr:
			xdelta = self.xcol.delta
			for i in range(0,len(xdelta)):
				xdelta[i] = withoutUnit(xdelta[i])
		else:
			xdelta = None
		if yerr:
			ydelta = self.ycol.delta
			for i in range(0,len(ydelta)):
				ydelta[i] = withoutUnit(ydelta[i])
		else:
			ydelta = None
		#print(xdelta)
		#print(ydelta)
		#x = [0,1,2,3,4]
		#y = [1,2,3,4,5]
		#yerr = [1,2,1,2,1]
		#self.ax.errorbar(x,y,yerr=yerr)
		#self.ax.errorbar(xColumn.withoutUnit(),yColumn.withoutUnit(), yerr=ydelta)
		#print(xColumn.dataForPlot())
		#print(yColumn.dataForPlot())
		startTime2 = millis()
		logFile.write("xPlt=" + listToString(xColumn.dataForPlot())+"\n")
		logFile.write("yPlt=" + listToString(yColumn.dataForPlot())+"\n")
		logFile.write("xdelta=" + listToString(xdelta)+"\n")
		logFile.write("ydelta=" + listToString(ydelta)+"\n")
		if "label" in kwargs:
			logFile.write("ax.errorbar(xPlt, yPlt, xerr=xdelta, yerr=ydelta)\n") #TODO **kwargs soll auch gelogt werden
			self.ax.errorbar(xColumn.dataForPlot(), yColumn.dataForPlot(), xerr=xdelta, yerr=ydelta, **kwargs)
		else:
			logFile.write("ax.errorbar(xPlt, yPlt, xerr=xdelta, yerr=ydelta, label=\"" + yColumn.textName() + "\")\n") #TODO **kwargs soll auch gelogt werden
			self.ax.errorbar(xColumn.dataForPlot(), yColumn.dataForPlot(), xerr=xdelta, yerr=ydelta, label=yColumn.textName(), **kwargs)
		if PROFILE:
			print(str(millis()-startTime2) + " ms for errorbar")
		if self.xcol.unit() != 1:
			logFile.write("ax.set_xlabel(\"" + self.xcol.textName() + " [$" + anythingExceptNumbersToTex(self.xcol.unit()) + "$]" + "\", usetex=True)\n")
			self.ax.set_xlabel(self.xcol.textName() + " [$" + anythingExceptNumbersToTex(self.xcol.unit()) + "$]", usetex=True)
		else:
			logFile.write("ax.set_xlabel(\"" + self.xcol.textName() + "\", usetex=True)\n")
			self.ax.set_xlabel(self.xcol.textName() , usetex=True)
		if self.ycol.unit() != 1:
			logFile.write("ax.set_ylabel(\"" + self.ycol.textName() + " [$" + anythingExceptNumbersToTex(self.ycol.unit()) + "$]" + "\", usetex=True)\n")
			self.ax.set_ylabel(self.ycol.textName() + " [$" + anythingExceptNumbersToTex(self.ycol.unit()) + "$]", usetex=True) #, fontsize=40
		else:
			logFile.write("ax.set_ylabel(\"" + self.ycol.textName() + "\", usetex=True)\n")
			self.ax.set_ylabel(self.ycol.textName() , usetex=True)
	def fitTest(self, sympy_fitfunc, subsdict, **kwargs): #TOOD: Document this funktion
		if isinstance(sympy_fitfunc, str):
			sympy_fitfunc = strToSympy(sympy_fitfunc)
		elif isinstance(sympy_fitfunc, Equation):
			if str(sympy_fitfunc.eqSympy.lhs) != self.ycol.memName:
				print("bad arguments for fitSym: sympy_fitfunc.lhs != self.ycol.memName")
				print(sympy_fitfunc.eqSympy.lhs)
				print(self.ycol.memName)
				exit(1)
			sympy_fitfunc = sympy_fitfunc.eqSympy.rhs
		sympy_fitfunc = sympy_fitfunc.subs(subsdict)#TODO einheiten checken
		sympy_fitfunc = sympy_fitfunc.subs(symbols(self.xcol.memName), symbols("x"))
		numpy_fitfunc = sympy.lambdify(symbols("x"), subsSIUnitsOne(sympy_fitfunc), "numpy")
		startX = self.xcol.dataForPlot()[0]
		stopX = self.xcol.dataForPlot()[-1]#Performance dataForPlot() gets called multiple times
		xdata = self.xcol.dataForPlot() #TODO das geht doch noch besser
		ydata = numpy_fitfunc(xdata)
		if isinstance(ydata, np.float64):
			#ydata = np.full(len(xdata),self.ycol.withoutUnit()) das war früher hier, aber ich glaube, dass das so falsch ist.
			ydata = np.full(len(xdata),ydata)
		if "label" in kwargs:
			self.ax.plot(xdata, ydata, **kwargs)
		else:
			self.ax.plot(xdata, ydata, label="Test", **kwargs)
	##Uses scipy.optimize.curve_fit to fit the function sympy_fitfunc to the data in self.xColumn and self.yColumn (if you want to know the origin of self.xColumn and self.yColumn look at the documentation of PlotLine.__init__ and Plot.add).
	##This Function is similar to PlotLine.fitSym, but there are 2 differences:
	## * The symbol of the x-asis value in sympy_fitfunc is "x" in fitX but xColumn.memName in fitSym
	## * If sympy_fitfunc is an instance of Equation, fitSym checks whether yColumn.memName and the left hand side of equation match. fitX does not accept an instance of Equation as sympy_fitfunc.
	##Example usuage (linear Fit for a particle that moves at constant speed)
	##\code{.py}
	#object.fitX( "speed*x + offset" , {speed: meter/second, offset: meter} )
	##\endcode
	##optimal fitparameters get stored in plotLine.poptSym and plotLine.poptStr
	##\param sympy_fitfunc Function used to fit. sympy_fitfunc shall only contain "x" and the fitparameters as free symbols. The type of sympy_fitfunc shall be a string or a sympy function
	##\param proposedUnits Sadly, you have to provide a dictionary with the units of every fitparameter. The function checks whether the units are correct. Sadly, only basic SI-Units are allowed.
	##\param **kwargs All additional arguments are passed to matplotlib.pyplot.plot
	def fitX(self, sympy_fitfunc, proposedUnits, **kwargs):
		startTime = millis()
		if isinstance(sympy_fitfunc, str):
			sympy_fitfunc = strToSympy(sympy_fitfunc)
		for i in proposedUnits:
			if subsSIUnitsOne(proposedUnits[i]) != 1:
				print("proposedUnits are not SI Units")
				exit(1)
			if isinstance(i,str):
				proposedUnits[symbols(i)] = proposedUnits.pop(i)
		for s in sympy_fitfunc.free_symbols:
			if s != symbols("x") and s not in proposedUnits:
				print("bad Arguments for fitX: " + str(s) + " is an unknown symbol.")
				print("The expression " + str(sympy_fitfunc) + " shouldn't contain any symbols except for x and the fitparameters:")
				for a in proposedUnits:
					print(a)
				exit(1)
		if checkGetUnit(toBasicSI(sympy_fitfunc.subs(proposedUnits).subs(symbols("x"),self.xcol.unit()))) != checkGetUnit(toBasicSI(self.ycol.unit())):
			print("wrong dimensions in fitfunc:")
			print(str(sympy_fitfunc) + " has dimension " + str(toBasicSI(checkGetUnit(sympy_fitfunc.subs(proposedUnits).subs(symbols("x"),self.xcol.unit())))))
			print("but ycol.unit is " + str(toBasicSI(self.ycol.unit())))
			exit(1)
		all_symbols = [symbols("x")]
		for s in sympy_fitfunc.free_symbols:
			if s != symbols("x"):
				all_symbols.append(s)
		numpy_fitfunc = sympy.lambdify(all_symbols, subsSIUnitsOne(sympy_fitfunc), "numpy")
		popt, pcov = scipy.optimize.curve_fit(numpy_fitfunc, self.xcol.dataForPlot(), self.ycol.dataForPlot());
		print(popt)
		print(pcov)
		print(np.sqrt(np.diag(pcov)))
		#startX = self.xcol.dataForPlot()[0]
		#stopX = self.xcol.dataForPlot()[-1]#Performance dataForPlot() gets called multiple times
		#xdata = np.arange(startX,stopX,(stopX-startX)/1000)
		xdata = self.xcol.dataForPlot() #TODO das geht doch noch besser
		ydata = numpy_fitfunc(xdata, *popt)
		if not xdata.shape == ydata.shape:
			ydata = np.full(len(xdata),ydata)
		#if isinstance(ydata, np.float64):
		#	#ydata = np.full(len(xdata),self.ycol.withoutUnit()) das war früher hier, aber ich glaube, dass das so falsch ist.
		#	ydata = np.full(len(xdata),ydata)
		if "label" in kwargs:
			self.ax.plot(xdata, ydata, **kwargs)
		else:
			self.ax.plot(xdata, ydata, label="Fit", **kwargs)
		self.poptSym = {}
		self.poptStr = {}
		for i in range(1, len(all_symbols)):
			self.poptSym[all_symbols[i]] = popt[i-1]*proposedUnits[all_symbols[i]]
			self.poptStr[str(all_symbols[i])] = popt[i-1]*proposedUnits[all_symbols[i]]
		if PROFILE:
			print(str(millis()-startTime) + " ms for fitX")
	##Uses scipy.optimize.curve_fit to fit the function sympy_fitfunc to the data in self.xColumn and self.yColumn (if you want to know the origin of self.xColumn and self.yColumn look at the documentation of PlotLine.__init__ and Plot.add).
	##This Function is similar to PlotLine.fitX, but there are 2 differences:
	## * The symbol of the x-asis value in sympy_fitfunc is "x" in fitX but xColumn.memName in fitSym
	## * If sympy_fitfunc is an instance of Equation, fitSym checks whether yColumn.memName and the left hand side of equation match. fitX does not accept an instance of Equation as sympy_fitfunc.
	##Example usuage (linear Fit for a particle that moves at constant speed)
	##\code{.py}
	#object.fitX( "speed*time + offset" , {speed: meter/second, offset: meter} )
	##\endcode
	##optimal fitparameters get stored in plotLine.poptSym and plotLine.poptStr
	##\param sympy_fitfunc Function used to fit. sympy_fitfunc shall only contain the fitparameters and xColumn.memName as free symbols. The type of sympy_fitfunc shall be a string or a sympy function
	##\param proposedUnits Sadly, you have to provide a dictionary with the units of every fitparameter. The function checks whether the units are correct. Sadly, only basic SI-Units are allowed.
	##\param **kwargs All additional arguments are passed to matplotlib.pyplot.plot
	def fitSym(self, sympy_fitfunc, proposedUnits, **kwargs):
		if isinstance(sympy_fitfunc, str):
			sympy_fitfunc = strToSympy(sympy_fitfunc)
		elif isinstance(sympy_fitfunc, Equation):
			if str(sympy_fitfunc.eqSympy.lhs) != self.ycol.memName:
				print("bad arguments for fitSym: sympy_fitfunc.lhs != self.ycol.memName")
				print(sympy_fitfunc.eqSympy.lhs)
				print(self.ycol.memName)
				exit(1)
			sympy_fitfunc = sympy_fitfunc.eqSympy.rhs
		self.fitX(sympy_fitfunc.subs(symbols(self.xcol.memName), symbols("x")), proposedUnits, **kwargs)
##Holds everything necessary to describe one diagramm
class Plot:
	##type(ax) is matplotlib.axes._subplots.AxesSubplot. Calling methods of ax is the recommended way of doing things like making the scale logarithmic, setting label for axes, ...
	ax = None
	#holds values of type PlotLine
	#lines = {}
	##Constructor. Sets self.ax to an instance of the class matplotlib.axes._subplots.AxesSubplot
	logFile = None
	def __init__(self, size=(7,5), display=False, logPath=None): #TODO den display Parameter und den logPath Parameter dokumentieren
		if PROFILE:
			startTime = millis()
		if logPath is not None:
			self.logFile = open(logPath, "w")
		else:
			self.logFile = open("/dev/null", "w")
		self.logFile.write("import matplotlib\n")
		self.logFile.write("import matplotlib.pyplot\n")
		self.lines = {}
		if display:
			self.fig = matplotlib.pyplot.figure(constrained_layout=True)
			self.logFile.write("fig = matplotlib.pyplot.figure(constrained_layout=True)\n")
		else:
			self.fig = matplotlib.figure.Figure(constrained_layout=True, figsize=size, dpi=1000)
			matplotlib.backends.backend_agg.FigureCanvasAgg(self.fig) #I'm not sure, but this is useless
			self.logFile.write("fig = matplotlib.pyplot.figure(constrained_layout=True, figsize=size, dpi=1000)\n")
			self.logFile.write("matplotlib.backends.backend_agg.FigureCanvasAgg(fig)\n")
		self.ax = self.fig.add_subplot(111) #alternative: .suplot( instead of .add_suplot(
		self.logFile.write("ax = fig.add_subplot(111)\n")
		#https://matplotlib.org/examples/ticks_and_spines/tick-locators.html
		#https://github.com/matplotlib/matplotlib/issues/8768
		#https://github.com/matplotlib/matplotlib/pull/12865
		if PROFILE:
			print(str(millis()-startTime) + " ms for Plot.__init__")
	##\snippet this Plot add
	def add(self, lineName, xColumn, yColumn, xerr=False, yerr=False, **kwargs):
		if PROFILE:
			startTime = millis()
		#! [Plot add]
		self.lines[lineName] = PlotLine(self.ax, self.logFile, xColumn, yColumn, xerr, yerr, **kwargs)
		#! [Plot add]
		if PROFILE:
			print(str(millis()-startTime) + " ms for Plot.add")
	##Saves the plot in a file
	##\param path Filepath of the graph. Has to include a correct file extension.
	def writeToFile(self, path):
		if PROFILE:
			startTime = millis()
		#self.ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
		#self.ax.yaxis.set_minor_locator(matplotlib.ticker.NullLocator())
		#self.ax.xaxis.set_major_locator(matplotlib.ticker.AutoLocator())
		#self.ax.yaxis.set_major_locator(matplotlib.ticker.AutoLocator())
		self.ax.legend()
		self.fig.savefig(path)
		if PROFILE:
			print(str(millis()-startTime) + " ms for Plot.writeToFile")
	##Saves the plot as a png and runs tex("\includegraphics[width=size\\textwidth]{path}")
	def showHere(self,size=1.0):
		if PROFILE:
			startTime = millis()
		self.ax.xaxis.set_major_locator(matplotlib.ticker.AutoLocator())
		self.ax.yaxis.set_major_locator(matplotlib.ticker.AutoLocator())
		self.ax.legend()
		for i in range(0,100):
			plot_path = os.path.join(_DATA_PATH_, str(i) + ".pdf") #.png does not work on my laptop
			if not os.path.exists(plot_path):
				self.fig.savefig(plot_path)
				tex("\\includegraphics[width=" + str(size) + "\\textwidth]{" + os.path.relpath(plot_path,start=os.path.dirname(_LATEX_PATH_))  +"}\\\\" )
				if PROFILE:
					print(str(millis()-startTime) + " ms for Plot.showHere")
				return
		print("unable to safe plot")
		exit(1)
	#! [Plot showAsFigure]
	##\snippet this Plot showAsFigure
	def showAsFigure(self, label, caption, size=1.0):
		tex("\\begin{figure}[H]")
		tex("\\centering")
		self.showHere(size)
		tex("\\caption{" + caption + "}")
		tex("\\label{" + label + "}")
		tex("\\end{figure}")
	#! [Plot showAsFigure]
	#! [Plot getitem]
	##\snippet this Plot getitem
	def __getitem__(self, key):
		return self.lines[key]
	#! [Plot getitem]
#    QASDAD, the quick and simple data analysis and documentation program
#    Copyright (C) 2018 Volker Weißmann . Contact: volker.weissmann@gmx.de

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

_TEX_FILE_ = None
_DATA_PATH_ = None
_LATEX_PATH_ = None
#def setTexFile(texfile):
#	_TEX_FILE_ = texfile
#def setDataPath(datapath):
#	_DATA_PATH_ = datapath
#def setLatexPath(latexpath):
#	_LATEX_PATH_ = latexpath

#! [tex]
##\snippet this tex
def tex(*args):
	for a in args:
		_TEX_FILE_.write(str(a)) #_TEX_FILE_ gets set by the qasdad executer.
#! [tex]
##Prints every part of a sympy expression. Only for debug purposes
def debugPrintExprArgs(expr):
	if len(expr.args) == 0:
		print(expr)
	else:
		for a in expr.args:
			debugPrintExprArgs(a)
##Convert a string to a sympy expression. Supports equal signs every unit from good_known_units_long
def strToSympy(expr):
	#expr = sympy.parsing.sympy_parser.parse_expr(expr)
	expr = sympy.parsing.sympy_parser.parse_expr(expr, transformations=(sympy.parsing.sympy_parser.standard_transformations + (sympy.parsing.sympy_parser.convert_equals_signs,)))
	#expr = sympy.sympify(expr)
	for u in good_known_units_long:
		expr = expr.subs(symbols(u), good_known_units_long[u])
	return expr
##Simpliflies an expression. E.g simplify(5*joule + 7*newton*meter) = 12*joule
def simplify(expr):
	print(expr)
##Check if table contains columns with len(data) == 1. If so, substitute the memName of the column with data[0] in expr
##\param expr: Accepts either a sympy expression or an instance of Equation as an argument.
##\param table: Accepts either a list, a dict or a table as an argument. (Note: The keys of the dictionary don't matter, the memName's do.)
def subsOneValColumn(expr, table):
	if isinstance(table, Table):
		table = list(table.cols.values())
	elif isinstance(table, dict):
		table = list(table.values())
	elif isinstance(table, list):
		pass
	else:
		print("bad argument for subsOneValColumn: table is not of 'Table' or 'dict' or 'list' Type")
		exit(1)
	if isinstance(expr, Equation):
		for c in table:
			if len(c.data) == 1:
				expr.eqSympy = expr.eqSympy.subs(c.memName, c.data[0])
	else:
		for c in table:
			if len(c.data) == 1:
				expr = expr.subs(c.memName, c.data[0])
	return expr
##Returns expr without the its. Note that it does not care whether the unit is a basic SI unit or not, use subsSIUnitsOne instead if you want to compare values. Note: It's probably super buggy and will (hopefully) be rewritten soon.
def withoutUnit(expr): #source: https://stackoverflow.com/questions/51119918/how-to-concisely-get-the-units-of-a-sympy-expression?rq=1
	try:
		float(expr)
		return expr
	except:
		pass
	#if isinstance(expr.evalf(), sympy.numbers.Float):
	#	return expr
	expr = 1.0*expr
	return float(expr.subs({x: 1 for x in expr.args if x.has(sympy.physics.units.Quantity)}))
##converts units and sympy expressions to nice formattet latex code. For Numbers use niceNumberPrintDigits and niceNumberPrintDelta instead
def anythingExceptNumbersToTex(expr):#https://stackoverflow.com/questions/23824687/text-does-not-work-in-a-matplotlib-label
	if isinstance(expr, str):
		expr = strToSympy(expr)
	#unit = sympy.latex(unit).replace(" ", "cdot ")
	expr = sympy.latex(expr)
	for u in good_known_units_short:
		expr = expr.replace(str(good_known_units_short[u]), "\\mathrm{" + u + "}")
	return expr
##Converts a value to a nicely formatted latex string
##\param digits: number of significant of digits
##\return Nicely formatted latex string e.g. 1,245\cdot 10^4 \\mathrm{m}
def niceNumberPrintDigits(value, digits):
	if isinstance(value, float):
		numValue = value
	else:
		numValue = withoutUnit(value)
	if numValue != 0:
		expValue = math.floor(math.log(abs(numValue), 10))
	else:
		expValue = 0
	ret = ""
	#ret += ("{:." + str(digits) +  "n}").format(numValue/10**expValue)
	ret += ( ("%." + str(digits) + "f") % (numValue/10**expValue) ).replace(".", ",")
	ret += "\cdot 10^{" + str(expValue) + "}"
	#if not isinstance(value,float):
	if checkGetUnit(value) != 1:
		ret += "\," + anythingExceptNumbersToTex(checkGetUnit(value))
	return ret
##Converts a value to a nicely formatted latex string
##\param delta: measurement uncertainty
##\return Nicely formatted latex string e.g. 1,245(1)\\cdot 10^4 \\mathrm{m}
def niceNumberPrintDelta(value, delta):
	if isinstance(value, float):
		numValue = value
		numDelta = delta
	else:
		numValue = withoutUnit(value)
		numDelta = withoutUnit(delta)
	if numValue != 0:
		expValue = math.floor(math.log(abs(numValue), 10))
	else:
		expValue = math.floor(math.log(abs(numDelta), 10))
	digits = expValue-math.floor(math.log(numDelta, 10))+1
	ret = ""
	#ret += ("{:." + str(digits) +  "n}").format(numValue/10**expValue)
	ret += ( ("%." + str(digits) + "f") % (numValue/10**expValue) ).replace(".", ",")
	ret += "(" + str(math.ceil(numDelta*10**(digits-expValue-1)))  + ")"
	ret += "\cdot 10^{" + str(expValue) + "}"
	#if not isinstance(value,float):
	if checkGetUnit(value) != 1:
		ret += "\," + anythingExceptNumbersToTex(checkGetUnit(value))
	return ret
def isnan(expr): #TODO diese Funktion dokumentieren
	if isinstance(expr, float):
		return math.isnan(expr)
	else:
		return expr == sympy.nan
	#if isinstance(expr, ):
	#	return math.isnan(expr)
##NumberFormat is a class that holds a specific way to print a value, eg Scientific Notation with 4 valid Digits and no uncertainty
class ValueFormat: #Why the f#@* does python not have real rust-like enums?
	##numDigits stores the number of valid digits that will be printed. If numDigits is 0 the number of digits that will be printed is inferred by the uncertainty of that value
	numDigits = 0
	##showDelta stores whether the uncertainty should be printed?
	showDelta = True
	#! [ValueFormat init]
	##\snippet this ValueFormat init
	def __init__(self, numDigits, showDelta):
		self.numDigits = numDigits
		self.showDelta = showDelta
	#! [ValueFormat init]
	##Returns the value "value" as a nice latex string. Acts if showDelta is False if delta is NaN. Crashes if value is NaN.
	def toNiceTexString(self, value, delta=None):
		ar = self.toNiceTexList(value, delta)
		ret = ""
		for s in ar:
			ret += s
		return ret
	##Length of the list returned by toNiceTexList
	listLength = 3 #TODO is it possible in python to declare this as static or constant
	##Similar to toNiceTexString, but splits the result into a list of the length "ValueFormat.listLength". E.g. ValueFormat(0,True).toNiceTexList(213,2) = ['2,130(2)', '\\cdot 10^{2}']
	def toNiceTexList(self, value, delta=None):
		ret = ["", "", ""]
		if delta is None and (self.showDelta == True or self.numDigits == 0):
			print("Bad arguments for toNiceTexList")
			exit(1)
		if isinstance(value, float):
			numValue = value
			numDelta = delta
		else:
			numValue = withoutUnit(value)
			numDelta = withoutUnit(delta) #PERFORMANCE: If numDigits is not 0 and showDelta is False
		if numValue != 0:
			expValue = math.floor(math.log(abs(numValue), 10))
		elif not isnan(delta):
			expValue = math.floor(math.log(abs(numDelta), 10))
		else:
			expValue = 1
		digits = self.numDigits
		if digits == 0:
			if not isnan(delta):
				digits = expValue-math.floor(math.log(numDelta, 10))+1
			else:
				digits = 3
		if numValue < 0:
			ret[0] = "-"
		ret[1] = ( ("%." + str(digits) + "f") % (abs(numValue)/10**expValue) ).replace(".", "{,}")
		if self.showDelta and not isnan(delta):
			ret[1] += "(" + str(math.ceil(numDelta*10**(digits-expValue-1)))  + ")"
		if expValue != 0:
			ret[2] += "\cdot 10^{" + str(expValue) + "}"
		if checkGetUnit(value) != 1:
			ret[2] += "\," + anythingExceptNumbersToTex(checkGetUnit(value))
		return ret
                
##Reads a file and returns a table
#File Format: e.g.\n
#\#text:time ;eq: x_1 ;eq: x_2\n
#\#s ; 0.0254*m ; 10**3*m\n
#10,35 1.00 0.796\n
#35.10 900 4,3\n
#The first line contains the memNames of the Coloumns: time, x_1 and x_2\n
#The "text" and "eq" specify whether the memName should be printed in a latex-text environment or a latex-math environment. For more information take a look at Column.mathName and Column.textName\n
#The second line gets multiplied with every line. This is useful for declaring units and 10^n's. For a total list of supported units look at good_known_units_short. SI unit prefixes are not supported. In this example, the first column would be in seconds, the second column in inch and the third column in kilometers.\n
#In the first two lines whitespaces get ignored if they are not within a memName\n
#From the third line onwards, both "," and "." have the same meaning, the decimal seperator.\n
#If this description of the file seems ambigious for you, take a look at the source code of this function.\n
#Security notice: readFile uses sympy.sympyfy which uses eval() which should not be used on untrusted input. Therefore, readFile(filepath) should only be run if filepath is at least as trustworthy as this script.
def readFile(filepath):
	if PROFILE:
		startTime = millis()
	with open(filepath) as fp:
		try:
			names = fp.readline().split(";")
			names[0] = names[0][1:]
			memNames = [name.split(":")[1] for name in names]
			memNames = [o.lstrip().rstrip() for o in memNames]
			nameType = [name.split(":")[0] for name in names]
			nameType = [o.lstrip().rstrip() for o in nameType]
		except:
			raise AssertionError("Exception in readFile: Ill-formed file: " + filepath)
		for n in nameType:
			if n != "eq" and n != "text":
				print("invalid file: nameType is neither eq, nor text")
				exit(1)
		units = fp.readline().split(";")
		units[0] = units[0][1:]
		units = [sympy.sympify(o).subs(good_known_units_short) for o in units]
	ret = Table()
	filestr = ""
	with open(filepath) as fp:  
		for line in fp:
			filestr += line.replace(";", "\t").replace(",", ".")
	if PROFILE:
		startTime2 = millis()
	matrix = np.loadtxt(io.StringIO(filestr), dtype=str)
	if PROFILE:
	        print(str(millis()-startTime2) + " ms for np.loadtxt")
	for i in range(0,len(matrix[0])):
		dat = [sympy.sympify(o)*units[i] for o in matrix[:,i]]
		delta=None
		delta = []
		for o in matrix[:,i]:
			ar = o.split(".")
			digits = 0
			if len(ar) == 2:
				digits = len(ar[1])
			delta.append(units[i]*10**(-digits)) 
		ret.add(Column(memNames[i],nameType[i],dat,delta=delta))
	if PROFILE:
		print(str(millis()-startTime) + " ms for readFile including np.loadtxt")
	return ret
##Prints table. Only for debug purposes Note: This function likes to crash.
def debugTableRaw(table):
	if not isinstance(table, Table):
		print("bad arguments for debugTableRaw: table is not an instance of class Table")
		exit(1)
	ret = "#"
	for a in table.cols:
		if table[a].memName != "_num":
			table[a].maxDataSpace = len(table[a].memName)
			table[a].maxDeltaSpace = 0
			for i in table[a].data:
				if len(str(i)) > table[a].maxDataSpace:
					table[a].maxDataSpace = len(str(i))
			if table[a].delta is not None:
				for i in table[a].delta:
					if len(str(i)) > table[a].maxDeltaSpace:
						table[a].maxDeltaSpace = len(str(i))
			ret += table[a].memName + " "*(1+table[a].maxDataSpace-len(table[a].memName) )
	#for i in self.data[0].data: das würde zu bugs nach führen wenn erst sort(), dann str() aufgerufen wird
	#len(table[0].data)
	maxLength = 0
	for a in table.cols:
		if len(table[a].data) > maxLength:
			maxLength = len(table[a].data)
	for i in range(0,maxLength): #TODO was wenn nicht alle Tabellen gleich lang sind
		ret += "\n "
		for a in table.cols:
#			if table[a].memName != "_num":
			#ret += str(a.data[i]) + " "*(1+a.maxDataSpace-len(str(a.data[i])) )
			if len(table[a].data) > i:
				msg = str(table[a].data[i])
			else:
				msg = "leer"
			ret += msg + " "*(1+table[a].maxDataSpace-len(msg) ) #+ "+- " +  str(table[a].delta[i]) + " "
			if table[a].delta is not None and len(table[a].delta) > i:
				msg = str(table[a].delta[i])
			else:
				msg = "leer"
			ret += "+- " + msg + " "*(1+table[a].maxDeltaSpace-len(msg) )
	print(ret)
##Prints table. Only for debug purposes Note: This function likes to crash.
def debugTableNice(table): #TODO: print(table) should execute this funktion
	if not isinstance(table, Table):
		print("bad arguments for debugTableNice: table is not an instance of class Table")
		exit(1)
	ret = "#"
	for a in table.cols:
		if table[a].memName != "_num":
			table[a].maxSpace = len(table[a].memName)
			for i in range(0,len(table[a].data)):
				length = len(niceNumberPrintDelta(table[a].data[i],table[a].delta[i]))
				if length > table[a].maxSpace:
					table[a].maxSpace = length
			ret += table[a].memName + " "*(1+table[a].maxSpace-len(table[a].memName) )
	#for i in self.data[0].data: das würde zu bugs nach führen wenn erst sort(), dann str() aufgerufen wird
	#len(table[0].data)
	maxLength = 0
	for a in table.cols:
		if len(table[a].data) > maxLength:
			maxLength = len(table[a].data)
	for i in range(0,maxLength): #TODO was wenn nicht alle Tabellen gleich lang sind
		ret += "\n "
		for a in table.cols:
#			if table[a].memName != "_num":
			#ret += str(a.data[i]) + " "*(1+a.maxSpace-len(str(a.data[i])) )
			if len(table[a].data) > i:
				msg = niceNumberPrintDelta(table[a].data[i],table[a].delta[i])
			else:
				msg = "leer"
			ret += msg + " "*(1+table[a].maxSpace-len(msg) ) #+ "+- " +  str(table[a].delta[i]) + " "
	print(ret)
##Uses the tex(...) command to show table as a a nicely formatted latex tabular
#\param table: Accepts either a list, a dict or a table as an argument. (Note: The keys of the dictionary don't matter, the memName's do.)
#\param format: Decides how the values should be printed. This argument should be a list of ValueFormat instances
#\param path: Writes the tabular into a file with the filepath "path"
def showAsTabular(table, format=None, path=None):
	if PROFILE:
		startTime = millis()
	if isinstance(table, Table):
		table = list(table.cols.values())
	elif isinstance(table, dict):
		table = list(table.values())
	elif isinstance(table, list):
		pass
	else:
		print("Bad argument for showAsTabular: table is not of 'Table' or 'dict' or 'list' Type")
		exit(1)
	if format is not None and not isinstance(format, dict):
		print("Bad argument for showAsTabular: format is neither None nor a 'dict'")
		exit(1)
	if path is not None:
		texfile = open(path, 'w')
	else:
		texfile = _TEX_FILE_
	texfile.write("\\begin{tabular}{" + (("l"*ValueFormat.listLength)+"|")*(len(table)-1) + "l"*ValueFormat.listLength + "}\n") #"r|"*(len(table)*ValueFormat.listLength-1)
	begin = True
	for c in table:
		if begin:
			begin = False
			texfile.write("\\multicolumn{" + str(ValueFormat.listLength) + "}{c}{")
		else:
			texfile.write("&\\multicolumn{" + str(ValueFormat.listLength) + "}{|c}{")
		texfile.write("$" + c.mathName() + "$") #TODO: Dokumentation anpassen
		if c.unit() != 1:
			texfile.write(" [$" + anythingExceptNumbersToTex(c.unit())  + "$]")
		texfile.write("}")
		#texfile.write("&"*(ValueFormat.listLength-1))
	texfile.write("\\\\\\hline\n")
	maxLength = 0
	for c in table:
		if len(c.data) > maxLength:
			maxLength = len(c.data)
	for i in range(0,maxLength):
		begin = True
		for c in range(0,len(table)):
			if begin:
				begin = False
			else:
				texfile.write("&")
			if len(table[c].data) > i:
				if format is not None and table[c].memName in format:
					fmt = format[table[c].memName]
				else:
					fmt = ValueFormat(0,False)
				if math.isnan(withoutUnit(table[c].data[i])):
					for i2 in range(1,ValueFormat.listLength):
						texfile.write("&\\hspace{-1em}")
				else:
					ar = fmt.toNiceTexList(withoutUnit(table[c].data[i]), withoutUnit(table[c].delta[i]))
					texfile.write("$" + ar[0] + "$")
					for i2 in range(1,len(ar)):
						texfile.write("&\\hspace{-1em}$" + ar[i2] + "$")
				#texfile.write("$" + fmt.toNiceTexString(withoutUnit(table[c].data[i]), withoutUnit(table[c].delta[i])) + "$")
				#texfile.write("$" + niceNumberPrintDelta( withoutUnit(c.data[i]), withoutUnit(c.delta[i]) ) + "$")
			else:
				texfile.write("&"*(ValueFormat.listLength-1))
		texfile.write("\\\\\n")
	texfile.write("\\end{tabular}\\\\")
	if path is not None:
		texfile.close()
	if PROFILE:
		print(str(millis()-startTime) + " ms for showAsTabular")
#! [showAsTable]
##\snippet this showAsTable
def showAsTable(table, label, caption, format=None):
	tex("\\begin{table}[H]")
	showAsTabular(table, format)
	tex("\\caption{" + caption + "}")
	tex("\\label{" + label + "}")
	tex("\\end{table}")
#! [showAsTable]
#    QASDAD, the quick and simple data analysis and documentation program
#    Copyright (C) 2018 Volker Weißmann . Contact: volker.weissmann@gmx.de

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

##Calculates a new Column from other Columns using a sympy equation
#Example usuage:
#col = calcColumn(table, "a + sin(b)", "c")
#this would calculate a Column col with the memName "c" and for every i the following equation would be true: col.data[i] = table["a"].data[i] + sin(table["b"].data[i])
#col.analPropUncert is a latex-string that holds the analytic propagation of uncertainty. Show with e.g. tex("$"+col.analPropUncert+"$")
#\param table: Accepts either a list, a dict or a table as an argument. (Note: The keys of the dictionary don't matter, the memName's do.)
#\param equation: The equation used to calculate the new column. Either a string, a sympy expression or an Equation is accepted.
#\param resultMemName: The memName of the calculated Column
#\param resultNameType: The nameType of the calculated Column
#\param resultMathName: The specialTexMathName of the calculated Column
#\param resultTextName: The specialTexTextName of the calculated Column
#\return: The calculated Column.
#Nice little Feature 1: If equation is an instance of Equation and resultMemName is None the memName of the calculated Column will be the left hand side of equation.
#Nice little Feature 2: If resultMathName is "equation" the specialTexMathName of the calculatedColumn is the latex representation of equation
#Nice little Feature 3: If resultTextName is "equation" the specialTexTextName of the calculatedColumn is the latex representation of equation
def calcColumn(table, equation, resultMemName=None, resultNameType="eq", resultMathName=None, resultTextName=None, examplePath=None):
	#TODO examplePath dokumentieren. Gucken ob das so die beste art und weise für das zurückgeben ist, oder ob calcColumn nicht besser eine Column und ein String zurückgeben sollte, o.ä.
	startTime = millis()
	if DEBUG:
		print("calcColumn called:")
		print("\ttable=", table)
		print("\tequation=", equation)
		print("\tresultMemName=", resultMemName)
		print("\tresultNameType=", resultNameType)
		print("\tresultMathName=", resultMathName)
		print("\tresultTextName=", resultTextName)
	willWeCalcExample = False
	if isinstance(equation, Equation):
		inverseDict = dict([[v,k] for k,v in equation.nameDict.items()])
		#(calcColumn(table, eq.eqSympy.rhs, str(eq.eqSympy.lhs), resultNameType="text", resultMathName=str(eq.eqSympy.lhs.subs(inverseDict)) ))
		resultMemName = str(equation.eqSympy.lhs)
		if resultMathName is None:
			resultMathName= str(equation.eqSympy.lhs.subs(inverseDict)) #TODO alternativ zu str(eq.eqSympy.lhs.subs(inverseDict)) könnte man doch auch den linken teil von eq.latex nehmen
		if resultTextName is None:
			resultTextName = "$" + resultMathName + "$"
		exampleEqLatex = equation.eqLatex
		equation = equation.eqSympy.rhs
		willWeCalcExample = True
	elif isinstance(equation, str):
		equation = strToSympy(equation)
	if resultMemName is None:
		print("bad argument for calcColumn: resultMemName is None")
		exit(1)
	if isinstance(table, Table):
		table = table.cols
	elif isinstance(table, dict):
		pass
	elif isinstance(table, list):
		table = {}
		for i in list:
			table[i.memName] = i
	else:
		print("bad argument for calcColumn: table has to of 'Table' or 'dict' or 'list' Type")
		exit(1)
	length = 1
	for a in table: #find length of all columns, store it in var length
		if length == 1 and len(table[a].data) != 1:
			length = len(table[a].data)
		elif length != len(table[a].data) and len(table[a].data) != 1:
			print("Fatal Error: Lengths don't match")
			exit(1)
	if resultMathName == "equation": #TODO das muss man dokumentieren, denn das weiß niemand von alleine
		resultMathName = sympy.latex(equation)
	if resultTextName == "equation": #TODO das muss man dokumentieren, denn das weiß niemand von alleine
		resultTextName = "$" + sympy.latex(equation) + "$"
	ret = Column(resultMemName, resultNameType, [], specialTexMathName=resultMathName, specialTexTextName=resultTextName)
	exampleRow = length-1
	if willWeCalcExample:
		exampleCalc = "Beispielrechnung für die Berechnung von $" + ret.mathName() + "$ in Abhängigkeit von:\\begin{itemize}"
		for co in table:
			if sympy.symbols(table[co].memName) in equation.free_symbols:
				if len(table[co].data) == 1:
					i = 1
				else:
					i = exampleRow
				exampleCalc += "\\item $" + table[co].mathName() + "=" + ValueFormat(0,False).toNiceTexString(table[co].data[i],table[co].delta[i])  +"$"
		exampleCalc += "\\end{itemize}\\begin{equation}\\begin{aligned}" + exampleEqLatex + "\\\\="
		exampleStep = exampleEqLatex.split("=")[-1]
	for i in range(0,length): #Alle bekannten Werte einsetzen
		eqcp = equation
		for a in table:
			if len(table[a].data) != 1:
				val = table[a].data[i]
				delta = table[a].data[i]
			else:
				val = table[a].data[0]
				delta = table[a].data[0]
			eqcp = eqcp.subs(table[a].memName, val)
			if willWeCalcExample and i == exampleRow:
				exampleStep = exampleStep.replace(table[a].mathName(), ValueFormat(0,False).toNiceTexString(val,delta))
		try:
			val = eqcp.evalf()
			val = sympy.physics.units.convert_to(val, checkGetUnit(val))
			ret.data.append(val)
		except:
			ret.data.append(-1)
			print("Fehler: Alle bekannten Größen wurden in die Gleichung eingesetzt, aber die Gleichung lässt sich trotzdem nicht zu einem float umformen. Die Gleichung ist:")
			print(equation)
			print("und bekannte Größen sind:")
			for a in table:
				print(table[a].memName)
			exit(1)
	#Ab hier sind alle Werte berechnet, alles ab hier ist fehlerrechnung
	#outfile = open(resultName+"_ff.tex","w")
	retFF = ""
	retFF += "\\begin{aligned}"
	retFF += "\\Delta " + ret.mathName()
	begin = True
	for co in table: #schreibt = delta x |df/dx| + delta y |df/dy| in die Datei
		if sympy.symbols(table[co].memName) in equation.free_symbols and not table[co].isDeltaZero():
			if begin:
				begin=False
				retFF += "="
			else:
				retFF += "+"
			retFF += "\\Delta " + table[co].mathName() + "\\left|\\frac{\\text d" + ret.mathName()  + "}{\\text d" + table[co].mathName() + "}\\right|"
	retFF += "\\\\"
	memNameMathNameDict = {} #zuordnung memName, mathName()
	for co in table:
		if sympy.symbols(table[co].memName) in equation.free_symbols:
			memNameMathNameDict[table[co].memName] =	table[co].mathName()
	diffDict = {} #symbolische Betragsableitungen
	for co in table: #diffDict berechen
		if sympy.symbols(table[co].memName) in equation.free_symbols and not table[co].isDeltaZero():
			diffDict[table[co].memName] = np.abs(sympy.diff(equation,sympy.symbols(table[co].memName)))
	begin = True
	for co in table: #schreibt = delta x |ableitung| + delta y |ableitung| in die Datei
		if sympy.symbols(table[co].memName) in equation.free_symbols and not table[co].isDeltaZero():
			if begin:
				begin=False
				retFF += "="
			else:
				retFF += "+"
			retFF += "\\Delta " + table[co].mathName() + sympy.latex(diffDict[table[co].memName].subs(memNameMathNameDict))
	retFF += "\\end{aligned}"
	#allNeededSymbols = [] #Liste aller symbole die es gibt aufstellen
	#for co in table:
	#	if sympy.symbols(table[co].memName) in equation.free_symbols:
	#		allNeededSymbols.append(table[co].memName)
	#vals = [] #Was wir für werte einsetzen werden
	#for sym in allNeededSymbols:
	#	vals.append(table[sym].data) #TODO Das macht probleme wenn table[c].memName  nicht memName ist
	#https://docs.sympy.org/latest/modules/numeric-computation.html
	#expr = sympy.symbols("ort")/sympy.symbols("zeit")
	#f = sympy.lambdify([sympy.symbols("ort"),sympy.symbols("zeit")], expr, "numpy")
	#o = np.array([1,2,3,4])
	#z = np.array([1,2,6,4])
	#t = [o,z]
	#print(f(*t))
	#exit(0)
	#diffLambdasDict = {} #alle Ableitungen als Lambdas schreiben
	#for d in diffDict:
	#	diffLambdasDict[d] = sympy.lambdify(allNeededSymbols, diffDict[d], "numpy")
	#diffNumDict = {}#alle Ableitungen mit zahlen eingesetzt
	#for d in diffDict:
	#	diffNumDict[d] = diffLambdasDict[d](vals) das funktioniert nicht wegen den Einheiten
	#print(diffNumDict)
	allSubs = [] #was allSubs ist findest du am besten mit print(allSubs) hinter dieser for-schleife heraus
	for i in range(0,length):
		allSubs.append({})
		for co in table:	
			if sympy.symbols(table[co].memName) in equation.free_symbols:
				if len(table[co].data) != 1:
					allSubs[i][table[co].memName] = table[co].data[i]
				else:
					allSubs[i][table[co].memName] = table[co].data[0]
	diffNumDict = {}
	for d in diffDict:
		diffNumDict[d] = []
		for i in range(0, length):
			diffNumDict[d].append(diffDict[d].subs(allSubs[i]).evalf())
	ret.delta = []
	for i in range(0,length):
		delt = 0
		for m in diffDict:
			delt += table[m].delta[i]*diffNumDict[m][i] #TODO das macht probleme wenn table[m].memName != m ist
			#print(table[m].delta[i]*diffNumDict[m][i])
		ret.delta.append(delt)
	ret.analPropUncert = retFF
	if willWeCalcExample:
		exampleCalc += exampleStep + "\\\\=" + ValueFormat(0, False).toNiceTexString(ret.data[exampleRow], ret.data[exampleRow]) + "\\end{aligned}\\end{equation}"
	if examplePath is not None:
		file = open(examplePath, "w")
		file.write(exampleCalc)
		file.close()
	if PROFILE:
		print(str(millis()-startTime) + " ms for calcColumn")
	return ret

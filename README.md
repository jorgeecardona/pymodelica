
# PyModelica

This project is intended to create a modelica simulator tool based on python tools, and higly integrateable with actual python scientific tools.

## RoadMap

* Create a basic parser of the 3.1 specification.
* Define the introspection process of a modelica entity from python.
* Define DAE Solver:

## GUI

* Something like Root: http://root.cern.ch/drupal/
* Matplotlib.
* 3d analysis.
* Changes models parameters from plots.
* a looks like flowcanvas widget.

## Solvers

There are a lot of solvers already implemented, we have to look the one that correctly fits, or even define a sort of interface to several solvers.
One approach could be to define a tiny solver, and then define an interface to others.

 * **SUNDIALS**: https://computation.llnl.gov/casc/sundials/main.html
 * **FiPy**: http://www.ctcms.nist.gov/fipy/
 * ...

## References
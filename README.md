# 169-bridge-optimizer

## Assumptions
These will change with research.
Assumptions simplify the project at some cost.
* The number of free points are fixed for each problem instance. (might not be true if doing some genetic shenanigans.)
* Trusses don't bend. (I don't think they're supposed to.)

## (Rough) Outline
* Programming Stuff
    * Bridge Object
        * Locations of free points
        * Material between two points
        * Cost Function
        * Maximum Stress Function

    * Constrained Optimizer
        * Unconstrained Optimizer
            * (assuming local search)
            * Descent Method
            * Line Search

    * Bridge Optimization
        * Create instance of optimization problem
            * Number of fixed points
            * Locations of fixed points
            * Number of free points
            * List of materials and their properties
        * Serialize result/process to file?

    * Visualizer
        * Import from file?
        * Maybe use as a front end too?

* Writeup
    * (Maybe do it in LaTeX? if everyone else is ok with it)
    * Problem Statement
    * Cite previous research
    * Decomposition (this outline, pretty much)
    * Experience coding
    * Results, Quantitative
        * Plots
    * Conclusions
    * Bibliography
    * Names!

* Poster
    * (maybe LaTeX)
    * cool pics
    * pics of awful bridges because they're funny

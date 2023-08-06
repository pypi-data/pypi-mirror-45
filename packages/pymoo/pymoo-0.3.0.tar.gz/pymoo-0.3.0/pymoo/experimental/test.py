from pymoo.optimize import minimize
from pymoo.algorithms.nsga2 import nsga2
from pymoo.util import plotting
from pymop.factory import get_problem

# load a test or define your own problem
problem = get_problem("zdt1")

# get the optimal solution of the problem for the purpose of comparison
pf = problem.pareto_front()

# create the algorithm object
method = nsga2(pop_size=100, elimate_duplicates=True)

# execute the optimization
res = minimize(problem,
               method,
               termination=('n_gen', 200),
               pf=pf,
               disp=True)

# plot the results as a scatter plot
plotting.plot(pf, res.F, labels=["Pareto-Front", "F"])
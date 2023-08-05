from collections import defaultdict

import cvxpy as cp
import numpy as np

IP_SOLUTION_OPTIMAL = 'optimal'
IP_SOLUTION_TIME_BOUND = 'time_bound'


class IPSolverParameters:

    def __init__(self,
        alpha_nu = 1000.0,
        alpha_llc = 10.0,
        alpha_l12 = 250.0,
        alpha_order = 1.0,
        alpha_prev = 10.0,
        burst_multiplier = 0.1,
        max_burst_pool_increase_ratio = 3.0,
        burst_core_colloc_usage_thresh = 0.5,
        weight_cpu_use_burst = 1.0):

        self.alpha_nu = alpha_nu
        self.alpha_llc = alpha_llc
        self.alpha_l12 = alpha_l12
        self.alpha_order = alpha_order
        self.alpha_prev = alpha_prev
        self.burst_multiplier = burst_multiplier
        self.max_burst_pool_increase_ratio = max_burst_pool_increase_ratio
        self.burst_core_colloc_usage_thresh = burst_core_colloc_usage_thresh
        self.weight_cpu_use_burst = weight_cpu_use_burst

    def __str__(self):
        return str(vars(self))

def optimize_ip(requested_cus, requested_cus_burst_pool, total_available_cus, num_sockets, previous_allocation=None,
        use_per_workload=None, solver_params=IPSolverParameters(),
        verbose=False, max_runtime_secs=1, tol_obj=1e-1, mip_gap=0.05, solver='GLPK_MI'):
    """
    This function will find the optimal placement of workloads on the compute units of the instance,
    potentially starting from an initial allocation state (in which case it will also try to minimize
    the changes required to the current placement to satisfy the new request). Optional burst pool
    can be specified, as well as a data-informed CPU usage per workload.
    The algorithm will strive to balance actual CPU usage per socket and core, and isolate
    the burst workload on different cores.

    Arguments:
        - requested_cus: array of integers representing the number of compute units requested by each workload. Ex: [2,4,8,4]
        - requested_cus_burst_pool: total minimum number of CUs requested in the burst pool
        - total_available_cus: total # of compute units on the instance
        - num_sockets: # of NUMA sockets on the instance
        - previous allocation: array of assignment vectors from a previous placement
        - use_per_workload: actual (or forecasted) CPU use per workload
        - burst_multiplier: extra boost to expand burst pool past requested amount
        - verbose: flag to turn on verbose output of the MIP solver
        - max_runtime_secs: the maximum runtime allowed to compute a solution (if supported by the solver)

    Returns:
        - an array of binary assignment vectors. For example: [[0, 1, 0, 0], [1, 0, 1, 0]] could be a possible
          return value for a call where requested_cus=[1, 2] and total_available_cus=4
          This would mean that the first workload was assigned the compute unit with index 1, and that
          the second workload was assigned the compute units with indices 0 and 3
        - status of the solution ("optimal" or "time_bound")
    """

    d = total_available_cus
    n = num_sockets
    c = d // 2  # number of physical cores
    b = total_available_cus // n  # number of CUs per socket
    k = len(requested_cus) + 1
    uk = k if requested_cus_burst_pool > 0 else k-1

    if sum(requested_cus) + requested_cus_burst_pool > d:
        raise ValueError("The total # of compute units requested is higher than the total available on the instance.")
    if total_available_cus % 2 != 0:
        raise ValueError("Odd number of compute units on the instance not allowed."
                         " we assume that there always are 2 hyper-threads per physical core.")

    r = np.array(requested_cus + [requested_cus_burst_pool])

    V = np.zeros((d, k), dtype=np.int32)
    for i in range(d):
        for j in range(k):
            V[i, j] = (i + 1) * (j + 1) * (i // b + 1)
    sV = np.sum(V)

    prev_M = None
    if previous_allocation is not None:
        prev_M = np.zeros((d, k), dtype=np.int32)
        for j, v in enumerate(previous_allocation):
            if j == k:  # means that previous one was bigger, we removed a task
                break
            for i in range(d):
                if v[i] > 0.5:
                    prev_M[i, j] = 1

    # Optimal boolean assignment matrix we wish to find
    # Last column is BURST
    M = cp.Variable((d, k), boolean=True)

    # Auxiliary variables needed
    X = cp.Variable((n, k), integer=True)
    Y = cp.Variable(c, integer=True)
    U = cp.Variable(1)
    Z = cp.Variable(c, boolean=True)

    # 1) Penalize placements where workloads span multiple sockets
    cost_NU = -(solver_params.alpha_nu / (n * k)) * cp.sum(X)

    # 2) Try to even the # of busy CPUs per socket
    cost_LLC = (solver_params.alpha_llc / n) * sum([cp.abs(U - cp.sum(M[t * b: (t + 1) * b, :])) for t in range(n)])

    # 3) Penalize full cores (because it means more L1/L2 trashing)
    cost_L12 = (solver_params.alpha_l12 / c) * cp.max(Y)

    # 4) Favor contiguous indexing for:
    # - better affinity of hyperthreads to jobs on the same core
    # - more organized placement
    cost_ordering = (solver_params.alpha_order / (d * k * sV)) * cp.sum(cp.multiply(V, M))

    # 5) Maximize the size of the burst pool
    cost_burst = -(solver_params.burst_multiplier / d) * cp.sum(M[:,k-1])

    # 6) [optional] if starting from a previous allocation,
    # penalize placements that move assignements too much
    # compared to reference placement.
    cost_prev = None
    if prev_M is not None:
        cost_prev = (solver_params.alpha_prev / (d * k)) * cp.sum(cp.abs(M - prev_M))

    # The placement has to satisfy the requested # of units for each workload
    CM1 = [cp.sum(M[:,j]) == r[j] for j in range(k-1)]
    if requested_cus_burst_pool > 0:
        CM1 += [cp.sum(M[:,k-1]) >= requested_cus_burst_pool]
        CM1 += [cp.sum(M[:,k-1]) <= solver_params.max_burst_pool_increase_ratio * requested_cus_burst_pool]
    else:
        CM1 += [cp.sum(M[:,k-1]) == 0]

    # Each compute unit can only be assigned to a single workload
    CM2 = [M * np.ones((k, 1)) <= np.ones((d, 1))]

    # Extra variables constraints (coming from linearization of min/-max operators)
    CX1 = [X[t, j] <= (1.0 / max(r[j], 1)) * cp.sum(M[t * b: (t + 1) * b, j]) for t in range(n) for j in range(uk)]
    CX2 = [X <= 1]

    CY1 = [Y[l] >= -1 + cp.sum(M[2 * l, :]) + cp.sum(M[2 * l + 1, :]) for l in range(c)]
    CY2 = [Y >= 0]

    CB =  []

    # Don't leave cores empty
    min_cores_req = np.sum(r[:-1]) + int(solver_params.max_burst_pool_increase_ratio * requested_cus_burst_pool)
    CC = [Z[l] <= cp.sum(M[2 * l : 2 * l + 1, :]) for l in range(c)] + [cp.sum(Z) >= min(min_cores_req, c)]

    if use_per_workload is not None:
        weights = np.ones((k,), dtype=np.float32)
        weights[-1] = solver_params.weight_cpu_use_burst
        for j, use in enumerate(use_per_workload):
            if not np.isnan(r[j]) and r[j] > 0:
                weights[j] = use / r[j]
            else:
                weights[j] = 1
        
        # Even CPU usage per core:
        CY2 = []
        CY1 = []
        TT = cp.Variable(1)
        RW1 = np.vstack([weights.T] * 2)
        cost_L12 = (solver_params.alpha_l12 / c) * sum([cp.abs(TT - cp.sum(cp.multiply(M[2 * t : 2 * t + 2, :], RW1))) for t in range(c)])

        if requested_cus_burst_pool > 0:
            ## Try not to collocate extra burst threads with static one if average CPU usage on core is above percentage treshold
            ZZ = cp.Variable(2 * c, boolean=True)
            CB += [ZZ[l] >= 0.5 * (M[2 * l + 1, k-1] * solver_params.weight_cpu_use_burst + cp.sum(cp.multiply(M[2 * l, :k-1], weights.T[:k-1]))) - solver_params.burst_core_colloc_usage_thresh for l in range(c)]
            CB += [ZZ[l + c] >= 0.5 * (M[2 * l, k-1] * solver_params.weight_cpu_use_burst + cp.sum(cp.multiply(M[2 * l + 1, :k-1], weights.T[:k-1]))) - solver_params.burst_core_colloc_usage_thresh for l in range(c)]
            cost_burst += 2000 * (solver_params.burst_multiplier / (2* c * (solver_params.weight_cpu_use_burst + 1e-6))) * cp.sum(ZZ)
        
        # Even CPU usage per socket:
        RW2 = np.vstack([weights.T] * b)
        cost_LLC = (solver_params.alpha_llc / n) * sum([cp.abs(U - cp.sum(cp.multiply(M[t * b: (t + 1) * b, :], RW2))) for t in range(n)])
        

    cost = cost_NU + cost_LLC + cost_L12 + cost_ordering + cost_burst
    if cost_prev is not None:
        cost += cost_prev

    constraints = CM1 + CM2 + CY1 + CY2 + CX1 + CX2 + CB + CC

    prob = cp.Problem(cp.Minimize(cost), constraints)

    if verbose:
        print("Number of scalar variables in problem: ", prob.size_metrics.num_scalar_variables)

    try:
        extra_args = {}
        if solver == 'GLPK_MI':
            extra_args = {
                "tm_lim": int(1000 * max_runtime_secs),
                "fp_heur": "GLP_ON",
                "ps_heur": "GLP_ON",
                "pp_tech": "GLP_PP_ALL",
                "bt_tech": "GLP_BT_BPH",
                "tol_obj": tol_obj,
                "mir_cuts": "GLP_ON",
                #"gmi_cuts" : "GLP_ON",
                #"cov_cuts": "GLP_ON",
                #"clq_cuts": "GLP_ON",
                "binarize": "GLP_ON",
                "presolve": "GLP_ON",
                "mip_gap": mip_gap,
                }
        elif solver == 'MOSEK':
            extra_args = {"mosek_params": {
                "MSK_DPAR_MIO_MAX_TIME": max_runtime_secs,
                "MSK_IPAR_NUM_THREADS": 1,
                "MSK_DPAR_MIO_TOL_REL_GAP": mip_gap
                }}
        elif solver == 'GUROBI':
            extra_args = {
                "TimeLimit": max_runtime_secs,
                "Threads": 2,
                "MIPGap": mip_gap,
                "ConcurrentMIP": 2,
                "PreSparsify": 1,
                "ImproveStartTime": 2 * max_runtime_secs/3
            }
        prob.solve(solver=solver, verbose=verbose, **extra_args)
    except Exception as e:
        msg = "Solver crashed. (requested_cus=%s , previous_allocation=%s)" % (
            requested_cus, previous_allocation)
        raise Exception(msg).with_traceback(e.__traceback__)

    if prob.status not in ('optimal', 'optimal_inaccurate'):
        raise Exception("Could not solve the integer program: `%s`" % (prob.status,))

    status = IP_SOLUTION_OPTIMAL if prob.status == 'optimal' else IP_SOLUTION_TIME_BOUND

    res = [None] * (len(requested_cus) + 1)
    for i, e in enumerate(M.value.T):
        res[i] = [1 if u > 0.5 else 0 for u in e]
    if verbose:
        if use_per_workload is None:
            weights = None
        print_statistics(res, use_per_workload, requested_cus_burst_pool, weights, k, c, n, b)

    if requested_cus_burst_pool == 0:
        res = res[:-1] 

    return res, status#, prob.value


def print_statistics(res, use_per_workload, requested_cus_burst_pool, weights, k, c, n, b):
    if requested_cus_burst_pool > 0:
        print("Burst pool size: requested=%s, allocated=%s" % (requested_cus_burst_pool, sum(res[-1])))
    if use_per_workload is not None:
        usage_per_core = []
        usage_per_core_burst = []
        for l in range(c):
            s = 0.0
            for j, alloc in enumerate(res):
                if j == k -1 :
                    continue
                if alloc[2 * l] == 1:
                    s += weights[j]
                if alloc[2 * l + 1] == 1:
                    s += weights[j]
            usage_per_core.append(s)

            s = 0.0
            if res[-1][2 * l] == 1:
                s += weights[j]
            if res[-1][2 * l + 1] == 1:
                s += weights[j]
            usage_per_core_burst.append(s)

        usage_per_core = np.array(usage_per_core)
        usage_per_core_burst = np.array(usage_per_core_burst)

        pr = lambda a, name: print("Usage per core (%s): avg=%.2f, std=%.2f, med=%.2f" % (
            name, np.mean(a), np.std(a), np.median(a)))

        pr(np.array([e for e in usage_per_core if e > 0]), "active, static")
        pr(np.array(usage_per_core), "static")
        if requested_cus_burst_pool > 0:
            pr(np.array([e for e in usage_per_core_burst if e > 0]), "active, burst")
            pr(np.array(usage_per_core_burst), "burst")
            pr(np.array([e for e in usage_per_core + usage_per_core_burst if e > 0]), "active, all")
            pr(usage_per_core + usage_per_core_burst, "all")

        usage_per_socket = []
        for t in range(n):
            s = 0.0
            for j, alloc in enumerate(res):
                for u in range(t * b, (t+1) * b):
                    if alloc[u] == 1:
                        s += weights[j]
            usage_per_socket.append(s)
        print("Usage per socket:", usage_per_socket)

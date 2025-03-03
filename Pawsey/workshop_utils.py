# some helper function definitions
# again we won't go into the details here but you will need to run the cell
# generic plotting library 
import matplotlib
import matplotlib.pyplot as plt
import mpl_interactions.ipyplot as iplt
matplotlib.logging.getLogger('matplotlib.font_manager').disabled = True
# import interactive widgets
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets
from IPython.display import display, Markdown, Latex
# import plotly 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.linalg import expm

# python utils 
import sys, os, subprocess
from timeit import default_timer as timer
import importlib
import argparse
import numpy as np
from typing import List, Dict, Tuple, Any

def check_python_installation(library : str):
    try:
        importlib.import_module(library)
        return True
    except ImportError:
        print(f"{library} is not installed.")
        return False

# set some paramters for plotting 
hfont = {'fontname':'Helvetica'}
plt.ioff() # let the interactive plot take over matplotlib interaction
plt.tight_layout()

def PlotPennyLaneHisto(results, plottitle : str = '') -> None:
    with plt.xkcd():
    # Based on "Stove Ownership" from XKCD by Randall Munroe
    # https://xkcd.com/418/

        # fig, ax = plt.subplots()
        fig = plt.figure(figsize=(7.5,7.5))
        ax = fig.add_axes((0.2, 0.2, 0.5, 0.5))
        ax.spines[['top', 'right']].set_visible(False)
        labels = [rf'$|{k}>$' for k in results.keys()]
        xvals = np.arange(len(results.keys()))
        yvals = [results[k] for k in results.keys()]
        ax.bar(labels, yvals, facecolor='DarkOrange', edgecolor='Gold', linewidth=4)
        ax.tick_params(axis='x', labelrotation=80)
        fig.show()

def _setupqubits(num_qubits, add_H, hqubits, add_CNOT, cnotqubits) -> None:
    qubits = [f'|{i}>' for i in range(1,num_qubits+1)]
    if not add_H:
        hqubits = []
    else:
        if hqubits == 'all':
            hqubits = qubits
        else:
            # parse the hqubit list to ensure that it works
            newhqubits = []
            for q in hqubits:
                if q >=0 and q<num_qubits:
                    newhqubits.append(qubits[q])
            if len(newhqubits)>0:
                hqubits = newhqubits 
            else:
                hqubits = qubits
    if not add_CNOT or len(qubits) == 1:
        cnotqubits = []
    else:
        if cnotqubits == 'default':
            cnotqubits = []
            for q in qubits[1:]:
                cnotqubits.append([qubits[0],q])

    return qubits, hqubits, cnotqubits 

def memcalc(
    ix , iy, 
    rep : str = 'state',
    add_gates : bool = False, 
    float_size : float = 8.0, 
):
    x = np.float64(ix)
    y = np.float64(iy)
    if rep == 'state':
        fac = 1.0
    elif rep == 'density':
        fac = 2.0
    else:
        fac = 1.0
    # mem is float size and memory to store vector/density matrix
    mem = np.log(2.0*float_size)+fac*x*np.log(2.0)
    # and if wanted to store gates then add more to memory 
    if add_gates: 
        mem += np.log(y) + 2.0*x*np.log(2.0)
    return mem

def flopcalc(
    ix, iy, iz, 
    rep : str = 'state', 
):
    x = np.float64(ix)
    y = np.float64(iy)
    z = np.float64(iz)
    if rep == 'state':
        flop = np.log(y * (2**(x+1)-1)*(2**x))+np.log(z)
    elif rep == 'density':
        flop = np.log(y * (2**(2*x)-1)*(2**(2*x)))+np.log(z)
    else:
        flop = np.log(y * (2**(x+1)-1)*(2**x))+np.log(z)
    return flop 

def _reportsim(num_qubits, num_gates, ireport : bool):

    if ireport:
        mem = np.exp(memcalc(num_qubits, num_gates)-3.0*np.log(1024))
        flops = np.exp(flopcalc(num_qubits, num_gates, 1))
        display(Markdown(f'### Computational cost'))
        display(Markdown(f'You have asked to simulate a circuit with {num_qubits} qubits and {num_gates} gates '))
        display(Markdown(f'* Memory: This would require {mem:.4f} GB of memory, or roughly {mem/8:.4f} laptops'))
        display(Markdown(f'* Operations: This would require {flops:.4e} Floating point operations per shot, or roughly {flops/5e12/128*0.5:.4e} seconds on a laptop'))

def PlotSystemRequirements(num_qubits : int = 2, num_gates : int = 1, num_measurements : int = 1, 
                          returnfig : bool = False):
    with plt.xkcd():
    # Based on "Stove Ownership" from XKCD by Randall Munroe
    # https://xkcd.com/418/
        
        mem = memcalc(num_qubits, num_gates)
        flops = flopcalc(num_qubits, num_gates, num_measurements)
        memlist = {
            'very small': np.log(0.01)+30.0*np.log(2),
            'Laptop': np.log(8)+30.0*np.log(2), 
            'GraceHopper node': np.log(456)+30.0*np.log(2), 
            'Setonix':np.log(0.5e6)+30.0*np.log(2),
            'El Capitan':np.log(5.3e6)+30.0*np.log(2),
            'All the storage on Earth':np.log(200e12)+30.0*np.log(2),
            'A few hundred Earths': np.log(1e16)+30.0*np.log(2),
        }
        flopslist = {
            '1s on a laptop': 5e12/128*0.5,
             '1s on a Supercomputer node':5e12,
             '1s on Setonix':42e15,
             '1s on El Capitan':1.8e18,
             '1s on all Google \ncloud computing': 3.98 * 1e21,
        }
        maxlognqubit = 9
        maxgates = 10
        x = 2**np.arange(maxlognqubit)
        fig, (ax1, ax2) = plt.subplots(2,1, figsize=(10,12))
        plt.subplots_adjust(left=0.4, right=0.95, top=0.9, bottom=0.1, hspace=0.4)
        ax1.plot(x, memcalc(x, num_gates), linewidth = 4, zorder = 2, color='cornflowerblue', marker='None')
        ax1.scatter([num_qubits], [memcalc(num_qubits, num_gates)], 
                   zorder = 3, facecolor='Navy', edgecolor='LightBlue', marker='o', s=100)
        ax1.plot([0,num_qubits], [mem, mem], 
                linewidth = 2, zorder = 1, color='lightblue', marker='None', linestyle='dashed')
        ax1.plot([num_qubits,num_qubits], [-2, mem], 
                linewidth = 2, zorder = 1, color='lightblue', marker='None', linestyle='dashed')
        ax1.set_xscale('log')
        ax1.set_xlim([1,2**(maxlognqubit+0.1)])
        ax1.set_ylim([-2, np.max([mem*1.1, (memlist['All the storage on Earth'])])])

        ax1.set_yticks([memlist[k] for k in memlist.keys()], 
                      labels=memlist.keys()) 
        ax1.set_xticks([1, 2, 4, 8, 16, 32, 64, 128, 256],
                      labels=['1', '2', '4', '8', '16', '32', '64', '128', '256']
                     ) 
        ax1.set_xlabel('Number of Qubits')
        ax1.set_ylabel('Amount of Memory')
        # ax1.set_title('How much does memory does it take to \nsimulate on a classical computer?')
        # fig.show()


        # fig2 = plt.figure()
        # ax2 = fig.add_axes((0.1, 0.1, 0.9, 0.9))
        ax2.plot(x, flopcalc(x, num_gates, num_measurements), linewidth = 4, zorder = 2, color='darkorange', marker='None')
        ax2.scatter([num_qubits], [flopcalc(num_qubits, num_gates, num_measurements)], 
                   zorder = 3, facecolor='darkgoldenrod', edgecolor='gold', marker='o', s=100)
        
        ax2.plot([0,num_qubits], [flops, flops], 
                linewidth = 2, zorder = 1, color='gold', marker='None', linestyle='dashed')
        ax2.plot([num_qubits, num_qubits], [-10, flops], 
                linewidth = 2, zorder = 1, color='gold', marker='None', linestyle='dashed')
        ax2.set_xscale('log')
        ax2.set_yticks([np.log(flopslist[k]) for k in flopslist.keys()], 
                      labels=flopslist.keys())
        ax2.set_xticks([1, 2, 4, 8, 16, 32, 64, 128, 256],
                      labels=['1', '2', '4', '8', '16', '32', '64', '128', '256']
                     ) 
        ax2.set_xlim([1,2**(maxlognqubit+0.1)])
        ax2.set_ylim([-10, np.max([flops*1.1, np.log(flopslist[list(flopslist.keys())[-1]])])])

        ax2.set_xlabel('Number of Qubits')
        ax2.set_ylabel('Amount of Time')
        # ax2.set_title('How long does it take to simulate \non a classical computer?')
        ax1.tick_params(axis='y', labelrotation=-1)
        ax2.tick_params(axis='y', labelrotation=-1)

        if returnfig: 
            return fig
        else:
            fig.show()

def _report_timings(
    api : str,
    n : int, 
    m : int, 
    s : int,
    runtimes, 
    verbose : bool 
):
    time = np.mean(runtimes)
    err = np.std(runtimes)
    tot = np.sum(runtimes)
    ni = len(runtimes)
    if verbose:
        display(Markdown(f'### Running {api} Circuit'))
        display(Markdown(f'You have asked to simulate a circuit with {n} qubits and {m} gates running {s} measurements'))
        display(Markdown(f'The runtime per {s} shots averaged over {ni} samples is ({time:.4g} +- {err:.2g}) s for total time of {tot:.4g}'))
    return [time, err, tot]

def _report_framework(algo : str, api : str, n : int, m : int):
    display(Markdown(f'## {algo} with {api} '))
    display(Markdown(f'Running {n} with {m} rounds of amplification'))


def GroversPennyLane(
    device = "default.qubit", 
    num_qubits : int = 3, 
    targets : List = [], 
    num_amplification : int = 2, 
    num_shots : int = 100, 
    num_iterations : int = 10, 
    report_system_requirements : bool = False,
    plot_circuit : bool = False,
    verbose : bool = True, 
    get_return : bool = True, 
):
    """
    Construct a grovers circuits and time it's speed
    """

    import pennylane as qml
    from pennylane import numpy as np
    
    api = f'PennyLane:{device}'
    if verbose: _report_framework("Grovers", api, num_qubits, num_amplification)

    if targets == []: 
        targets = [np.ones(num_qubits, dtype=int)]

    # circuit     
    dev = qml.device(device, wires=num_qubits, shots = num_shots, )
    @qml.qnode(dev)
    def circuit(n, targets, m):
        wires = list(range(n))
        for i in range(n):
            qml.Hadamard(i)
        for _ in range(m):
            for t in targets:
                qml.FlipSign(t, wires=wires)  # apply the oracle
        qml.GroverOperator(wires)  # apply Grover's operator

        return [qml.expval(qml.PauliZ(i)) for i in range(n)]  # measure qubits

    specs_func = qml.specs(circuit)
    specs = specs_func(num_qubits, targets, num_amplification)
    num_gates = specs['resources'].num_gates

    _reportsim(num_qubits, num_gates, report_system_requirements)
    # plotting circuit
    if plot_circuit:
        fig, ax = qml.draw_mpl(circuit, show_all_wires=True)(num_qubits, targets, num_amplification)
        fig.show()
    
    # now run 
    runtimes = np.zeros(num_iterations)
    for i in range(num_iterations):
        start = timer()
        results = circuit(num_qubits, targets, num_amplification)
        end = timer()
        runtimes[i] = end-start
    
    [time, err, tottime] = _report_timings(api = api, n = num_qubits, m = num_gates, s = num_shots, runtimes = runtimes, verbose = verbose)
    if get_return :
        return [circuit, time, err, tottime]
    else:
        return


def GroversQiskit(
    device = "CPU", 
    num_qubits : int = 3, 
    targets : List = [], 
    num_amplification : int = 2, 
    num_shots : int = 100, 
    num_iterations : int = 10, 
    report_system_requirements : bool = False,
    plot_circuit : bool = False,
    verbose : bool = True, 
    get_return : bool = True, 
):
    """
    Construct a grovers circuits and time it's speed
    """

    from qiskit import QuantumCircuit, transpile
    from qiskit.circuit.library import GroverOperator, MCMT, ZGate
    from qiskit_aer import AerSimulator

    sim_ideal = AerSimulator(method='statevector', device=device)

    api = f'Qiskit:{device}'
    if verbose: _report_framework("Grovers", api, num_qubits, num_amplification)

    # sampler = Sampler(mode=backend)
    # sampler.options.default_shots = num_shots

    if targets == []: 
        targets = [''.join(["1" for i in range(num_qubits)])]
    # circuit
    def grover_oracle(num_qubits, targets):
        qc = QuantumCircuit(num_qubits)
        # Mark each target state in the input list
        for target in targets:
            # Flip target bit-string to match Qiskit bit-ordering
            rev_target = target[::-1]
            # Find the indices of all the '0' elements in bit-string
            zero_inds = [ind for ind in range(num_qubits) if rev_target.startswith("0", ind)]
            # Add a multi-controlled Z-gate with pre- and post-applied X-gates (open-controls)
            # where the target bit-string has a '0' entry
            if len(zero_inds) > 0:
                qc.x(zero_inds)
            qc.compose(MCMT(ZGate(), num_qubits - 1, 1), inplace=True)
            if len(zero_inds) > 0:
                qc.x(zero_inds)
        return qc
    # get the oracle circuit and construct an operator from this circuit
    oracle = grover_oracle(num_qubits, targets)
    grover_op = GroverOperator(oracle)
    # construct the base circuit, initalize superposition state
    circuit = QuantumCircuit(num_qubits)
    circuit.h(range(num_qubits))
    # Apply Grover operator the optimal number of times
    circuit.compose(grover_op.power(num_amplification), inplace=True)
    # Measure all qubits
    circuit.measure_all()
    # transpile for ideal state simulation
    circuit = transpile(circuit, sim_ideal)

    num_gates = circuit.size()
    _reportsim(num_qubits, num_gates, report_system_requirements)

    if plot_circuit:
        circuit.draw(output="mpl", style="iqp")
    
    # now run 
    runtimes = np.zeros(num_iterations)
    for i in range(num_iterations):
        start = timer()
        result = sim_ideal.run(circuit).result()
        end = timer()
        runtimes[i] = end-start
    
    [time, err, tottime] = _report_timings(api = api, n = num_qubits, m = num_gates, s = num_shots, runtimes = runtimes, verbose = verbose)
    if get_return :
        return [circuit, time, err, tottime]
    else:
        return


def GroversCUDAQ(
    device = "nvidia", 
    num_qubits : int = 3, 
    targets : List = [], 
    num_amplification : int = 2, 
    num_shots : int = 100, 
    num_iterations : int = 10, 
    report_system_requirements : bool = False,
    plot_circuit : bool = False,
    verbose : bool = True, 
    get_return : bool = True, 
):
    """
    Construct a grovers circuits and time it's speed
    """

    libcheck = check_python_installation('cudaq')
    if libcheck == False:
        print('CUDAQ not found! Returning no circuit and empty arrays')
        return [None, np.array([]), np.array([]), np.array([])]
    import cudaq

    if targets == []: 
        targets = [np.ones(num_qubits, dtype=int)]

    if cudaq.num_available_gpus() == 0:
        device = 'cpu'
    cudaq.set_target(device)
    
    api = f'CUDAQ:{device}'
    if verbose: _report_framework("Grovers", api, num_qubits, num_amplification)

    # Define our kernel.
    @cudaq.kernel
    def kernel(n, targets, m):
        # Initialize state
        qvector = cudaq.qvector(n)
        h(qvector)
    
        for i in range(m):
            # Mark
            # need to generalize for targets
            # for t in targets
            z.ctrl(qvector[:-1], qvector[-1])
    
            # Diffusion
            h(qvector)
            x(qvector)
            z.ctrl(qvector[:-1], qvector[-1])
            x(qvector)
            h(qvector)
        # measure 
        mz(qvector)

        
    num_gates = num_qubits + num_amplification*(num_qubits*4 + (num_qubits-1)*2)
    _reportsim(num_qubits, num_gates, report_system_requirements)
    
    # now run 
    runtimes = np.zeros(num_iterations)
    for i in range(num_iterations):
        start = timer()
        result = cudaq.sample(kernel, num_qubits, targets, num_amplification, shots_count=num_shots)
        end = timer()
        runtimes[i] = end-start
    
    [time, err, tottime] = _report_timings(api = api, n = num_qubits, m = num_gates, s = num_shots, runtimes = runtimes, verbose = verbose)
    return [None, time, err, tottime]


def _maketarget(rows, cols, irand):
    if (rows < 2): rows = 2
    if (cols < 2): cols = 2
    x_target, y_target = rows/2, cols/2
    if (irand):
        x_target, y_target = np.random.randint(low = 1, high = 5, size = 2)

    x = [j + 1 for i in range(rows) for j in range(cols)]
    y = [i + 1 for i in range(rows) for j in range(cols)]
    return rows, cols, x_target, y_target, x, y


def GroversGrid(rows: int = 4, cols : int = 4, irand : bool = True, 
               msize = 50 ):
    '''
    @brief generate a grid and have people try to find the target
    '''
    colorset = {'Hit': '#bae2be', 'Miss': 'White', 'Off': '#a3a7e4'}
    bbox = dict(boxstyle="round", fc="white", ec='black')
    def update_point(trace, points, selector):
        c = list(scatter.marker.color)
        s = list(scatter.marker.size)
        for i in points.point_inds:
            if x[i] == x_target and y[i] == y_target:  
                c[i] = colorset['Hit'] 
            else:
                c[i] = colorset['Miss']
            s[i] = 50
        with figwidget.batch_update():
            scatter.marker.color = c
            scatter.marker.size = s    
            ntries = list(scatter.marker.color).count(colorset['Miss'])
            if colorset['Hit'] in c:
                figwidget.update_layout(title = f"\nSuccess! In {ntries+1} tries.")
            else:
                figwidget.update_layout(title = f"\nNumber of misses = {ntries+1} of {len(c)}.")

    # initialize the target state
    rows, cols, x_target, y_target, x, y = _maketarget(rows, cols, irand)

    # create interative plotly figure
    figwidget = go.FigureWidget([go.Scatter(x=x, y=y, mode='markers')])
    scatter = figwidget.data[0]
    colors = [colorset['Off']] * (rows * cols)
    scatter.marker.color = colors
    scatter.marker.size = [msize] * (rows * cols)
    figwidget.layout.hovermode = 'closest'
    # update the layout 
    figwidget.update_layout(
        width=(2.05*msize)*(rows+1),  
        height=(2.05*msize)*(cols+1),
        xaxis=dict(
            scaleanchor='y',
            scaleratio=1,
            range=[0, cols + 1],
            showticklabels=False,  
            tickvals=[],          
        ),
        yaxis=dict(
            range=[0, rows + 1],
            showticklabels=False,  
            tickvals=[],           
        ),
        plot_bgcolor='white',  
        paper_bgcolor='white',
        title=f"Where's the hidden target?",
    )
    figwidget.update_traces(marker=dict(
                              line=dict(width=2,
                                        color='DarkSlateGrey')),
                            )
    scatter.on_click(update_point)
    return figwidget


def GroverSearch(rows: int = 4, cols : int = 4, irand : bool = True, 
                 figwidth : int = 500, figheight : int = 750, 
                 jitter_strength : float = 0.0015):
    '''
    @brief show a grover's search where data is displayed in a grid and try to show how size of target increased by grovers search

    '''

    colorset = {'Hit': '#bae2be', 'Miss': 'DarkOrange', 'Off': '#a3a7e4'}
    rows, cols, x_target, y_target, x, y = _maketarget(rows, cols, irand)
    n = rows * cols     
    target = n/2+1
    if irand: target = np.random.randint(low = 0, high = n)
    
    def prob(phase, ts, target, n):
        G = np.ones((n, n)) - np.eye(n)
        psi = (1/np.sqrt(n)) * np.ones(n, dtype=np.complex128)
        psi[0] *= np.exp(1j * phase)
        return [np.abs((expm(-1j * t * G) @ psi)[target])**2 for t in ts]
    
    def target_term(phase, t, n):
        return np.exp(1j * (n-1) * t)*[(1/np.sqrt(n))*np.exp(-1j * phase)]
    
    def non_target_term(phase, t, n):
        return (1/np.sqrt(n)) * (n-1) * np.exp(1j * (n-1) * t)*(np.exp(-1j * n * t) - 1)*(1/(n))*np.exp(-1j * phase)
    
    ts = np.arange(0, 1, 0.01)
    phis = np.linspace(0, 2 * np.pi, 100)  
    
    fig = make_subplots(
        rows=2, cols=2, shared_xaxes='columns',
        subplot_titles=("Probability of Measuring the Target", "Relative Probability", "Amplitude Contributions", None),
        specs=[
            [{"type": "xy"}, {"type": "xy", "rowspan": 2}], 
            [{"type": "xy"}, None]                           
        ],
    )
    
    
    phi = 0
    
    colors = [colorset['Miss']] * n
    colors[target] = colorset['Hit']  
    
    marker_sizes = n * [int(500 / n)]
        
    y_prob = prob(0, ts, 0, n)
    y_prob_jittered = y_prob + np.random.normal(0, jitter_strength, size=len(y_prob))
    
    y_target_term = np.abs(target_term(0, ts, n)) * np.real(target_term(0, ts, n))
    y_target_term_jittered = y_target_term + np.random.normal(0, jitter_strength, size=len(y_target_term))
    
    y_non_target_term = np.abs(non_target_term(0, ts, n)) * np.imag(non_target_term(0, ts, n))
    y_non_target_term_jittered = y_non_target_term + np.random.normal(0, jitter_strength, size=len(y_non_target_term))
    
    trace1 = go.Scatter(
        x=ts,
        y=y_prob_jittered,
        mode='lines',
        line=dict(color=colorset['Hit'], width=4, dash='solid'),
        name="Probability to Measure the Target",
        line_shape='spline'
    )
    
    trace2 = go.Scatter(
        x=ts,
        y=y_target_term_jittered,
        mode='lines',
        line=dict(color=colorset['Hit'], width=4, dash='solid'),
        name="Amplitude from the Target",
            line_shape='spline'
    )
    
    trace3 = go.Scatter(
        x=ts,
        y=y_non_target_term_jittered,
        mode='lines',
        line=dict(color=colorset['Miss'], width=4, dash='dash'),
        name="Amplitude From Other States",
        line_shape='spline'
    )
    
    trace4 = go.Scatter(
        x=x, y=y, mode='markers',
        name = "Relative Probability", 
        marker=dict(size=marker_sizes, color=colors)
    )
    
    fig.add_trace(trace1, row=1, col=1)
    fig.add_trace(trace2, row=2, col=1)
    fig.add_trace(trace3, row=2, col=1)
    fig.add_trace(trace4, row=1, col=2)
    
    steps = []
    for phi in phis:
        y_prob = prob(phi, ts, 0, n)
        y_prob_jittered = y_prob + np.random.normal(0, jitter_strength, size=len(y_prob))
    
        y_target_term = np.abs(target_term(phi, ts, n)) * np.real(target_term(phi, ts, n))
        y_target_term_jittered = y_target_term + np.random.normal(0, jitter_strength, size=len(y_target_term))
    
        y_non_target_term = np.abs(non_target_term(phi, ts, n)) * np.imag(non_target_term(phi, ts, n))
        y_non_target_term_jittered = y_non_target_term + np.random.normal(0, jitter_strength, size=len(y_non_target_term))
    
        marker_sizes = np.empty(n, dtype=int)
        marker_sizes[:] = int(500 * prob(phi, [ts[np.argmax(prob(phi, ts, 1, n))]], 1, n)[0])
        marker_sizes[target] = int(500 * prob(phi, [ts[np.argmax(prob(phi, ts, 0, n))]], 0, n)[0])
        step = dict(
            method="update",
            args=[
                {
                    "y": [
                        y_prob_jittered,
                        y_target_term_jittered,
                        y_non_target_term_jittered,
                        y
                    ],
                    "marker": [
                        None,
                        None,
                        None,
                        {"size": marker_sizes, "color": colors, "linecolor": 'DarkSlateGrey', "linewidth": 2}
                    ]
                }
            ],
            label=f"{np.degrees(phi):.0f}°"  
        )
        steps.append(step)
    
    sliders = [dict(
        active=0,  
        pad={"t": 50},
        steps=steps,
        currentvalue={"prefix": "Phase angle between target and non-target states: "}
    )]
    
    fig.update_yaxes(range=[0, 2.0/np.sqrt(n)], row=1, col=1)
    fig.update_yaxes(range=[-1.2/np.sqrt(n), 1.2/np.sqrt(n)], row=2, col=1)
    
    
    fig.update_xaxes(showticklabels=False, row=1, col=2)
    fig.update_yaxes(showticklabels=False, row=1, col=2)
    
    #fig.update_xaxes(title_text='time', row=2, col=1)
    
    
    fig.update_layout(
        sliders=sliders,
        width=2 * figwidth, height=figheight,
        showlegend=False,   
        margin=dict(t=50),   
        font=dict(family="Comic Sans MS, sans-serif", size=16, color="black"),
        plot_bgcolor='white',
        xaxis=dict(showgrid=False, zeroline=True, zerolinewidth=2, zerolinecolor='Black'),
        yaxis=dict(showgrid=True, zeroline=True, zerolinewidth=2, zerolinecolor='Black'),
        xaxis3=dict(showgrid=False, zeroline=True, zerolinewidth=2, zerolinecolor='Black'),
        yaxis3=dict(showgrid=True, zeroline=True, zerolinewidth=2, zerolinecolor='Black'),
    )
    fig.update_traces(marker=dict(line=dict(width=2, color='DarkSlateGrey')),)
    
    fig.update_xaxes(showgrid=False, row=1, col=1)
    fig.update_yaxes(showgrid=False, row=1, col=1)
    
    xaxis_domain = fig.layout.xaxis2.domain
    yaxis_domain = fig.layout.yaxis2.domain
    
    fig.add_shape(
        type="rect",
        xref="paper",
        yref="paper",
        x0=xaxis_domain[0],
        y0=yaxis_domain[0],
        x1=xaxis_domain[1],
        y1=yaxis_domain[1],
        fillcolor="white",
        #line=dict(width=0),
        layer="below"
    )
    return fig


def RunGrovers(b : str, 
               q : int, 
               n : str, 
               nt : int = 1, 
               rerun : bool = True, 
               my_env = os.environ.copy()
              ) -> Tuple[str, str]:
    basename = f'output/{b}.nqubits-{q}.noise-{n}'
    outname = f'{basename}.out'
    logname = f'{basename}.log'
    cmd = f'./grovers/bin/grovers_cudaq_{b} -n {q} -d {n} -t {nt} -o {outname}'.split(' ')
    if rerun or (not rerun and not os.path.isfile(logname)):
        print(f'Running {b}, Qubit {q}, Noise {n}, Num Trajectories {nt} ...')
        with open(logname, "w") as f:
            subprocess.run(cmd, stdout=f, env=my_env)
        print(f'Done')
    return outname, logname 

def _get_time_in_seconds(t : float, u : str) -> float:
    if u == '[ns]' : t *= 1e-9
    elif u == '[us]' : t*= 1e-6
    elif u == '[ms]' : t*= 1e-3
    elif u == '[min]' : t*= 60.0
    return t

def _get_mem_in_GB(m : float, u : str) -> float:
    if u == '[GiB]' : m *= 1
    elif u == '[MiB]' : m*= 1e-3
    elif u == '[KiB]' : m*= 1e-6
    return m

def ParseProfilingOutput(fname : str ) -> Dict[str, Any]:
    data = {'cpu' : 
            {'time' : 0, 'usage' : np.zeros(4), 'mem': 0},
            'gpu' : 
            {'time' : 0, 'usage' : np.zeros(4), 'mem': np.zeros(4)},
           }
    with open(fname) as f:
        lines = f.readlines()
        for l in lines:
            if 'Time taken between' in l:
                time = float(l.strip().split(' ')[-2])
                unit = (l.strip().split(' ')[-1])
                t = _get_time_in_seconds(time, unit)
                data['cpu']['time'] = t
            if 'Time taken on device between' in l:
                time = float(l.strip().split(' ')[-2])
                unit = (l.strip().split(' ')[-1])
                t = _get_time_in_seconds(time, unit)
                data['gpu']['time'] = t
            if 'Memory report @ main grovers_cudaq.cpp' in l:
                val = l.strip().split('VM current/peak:')[-1].split('; RSS current/peak:')[-1].split(' ')
                m = _get_mem_in_GB(float(val[-2]), val[-1])
                data['cpu']['mem'] = m
            if 'CPU Usage ' in l:
                val = l.strip().replace(',', '').replace('[','').replace(']','').split(' ')[-5:-1:1]
                data['cpu']['usage'] = np.array([np.float32(v) for v in val])
            if 'GPU Statistics ' in l:
                vals = l.strip().split(' || ')[1:]
                v = vals[0]
                val = v.replace(',', '').replace('[','').replace(']','').split(' ')[-6:-2:1]
                data['gpu']['usage'] = np.array([np.float32(v) for v in val])
                v = vals[1]
                val = v.replace(',', '').replace('[','').replace(']','').split(' ')[-6:-2:1]
                data['gpu']['mem'] = np.array([np.float32(v) for v in val])
            if 'Number of gates in circuit' in l:
                val = l.strip().split(' ')[-1]
                data['gates'] = int(val)
    return data
        

# Let's examine the results. 
def visualise_bitstring_counts(files : List[str], min_count=2) -> None:
    """
    Visualise bitstring counts greater than or equal to min_count
    from up to two output files on a bar chart.
    """
    def load(filename : str):
        data = {}
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                key, value = line.split(' : ')
                data[key.strip()] = int(value.strip())
        return data
    data = dict()
    counts = dict()
    labels = dict()
    norm = dict()
    for f in files:
        data[f] = load(f)
        norm[f] = 1.0/np.sum([cnt for bit, cnt in data[f].items()])
        labels[f] = f.replace('output/','').replace('.out','')
        data[f] = {bit: cnt for bit, cnt in data[f].items() if cnt >= min_count}
    # Get the union of all bitstrings from all files
    all_bitstrings = sorted(set(data[files[0]].keys()))
    for f in files:
        all_bitstrings = sorted(set(all_bitstrings) | set(data[f].keys()))
    for f in files:
        counts[f] = np.array([data[f].get(bit, 0) for bit in all_bitstrings], dtype=np.float32)

    x = np.arange(len(all_bitstrings))
    width = 1.0  # Width of each bar

    fig, ax = plt.subplots(figsize=(12, 6))
    multiplier = 0 
    for f in files:
        offset = width * multiplier/len(files)
        ax.bar(x - width/(2.0) + offset, counts[f]*norm[f], width/len(files), 
               label=f'{labels[f]}', edgecolor='k', alpha=0.5)
        multiplier += 1 

    ax.set_xlabel("Bitstrings")
    ax.set_ylabel("Probability")
    ax.set_title(f"Probability by Bitstring (min_count = {min_count})")
    ax.set_xticks(x)
    ax.set_xticklabels(all_bitstrings, rotation=90)
    ax.legend()

    plt.tight_layout()
    plt.show()

def visualise_profiling_ideal(data : Dict[str, Any], 
                        backends : List[str] = [], 
                        noises : List[str] = ['0.0'], 
                        ) -> None:
    """
    Scatter plot of CPU and GPU statistcs, like time taken, cpu usage, gpu usage and memory
    """
    #ideal = '0.0'
    basemarkerset = ['o', 's', 'v', '^', '*', '+', 'x']
    markerset = dict()
    for i in range(len(noises)):
        markerset[noises[i]] = basemarkerset[i]
    
    npanels = 5
    fig = plt.figure(figsize=(12, 3*npanels))
    gs = plt.GridSpec(npanels, 1, figure=fig, hspace=0.0)
    if len(backends) == 0: backends = list(data.keys())

    ax = fig.add_subplot(gs[0, 0])
    for b in backends:
        qubits = np.array(list(data[b].keys()))
        for n in noises: 
            yval = list()
            for q in qubits:
                yval.append(data[b][q][n]['cpu']['time'])
            yval = np.array(yval)
            ax.scatter(qubits, yval, 
                       alpha=0.5, zorder = 10, edgecolor = 'k', s = 150, 
                       label = f'{b}.noise-{n}', 
                       marker = markerset[n],
                      )
            ax.plot(qubits, yval, 
                    alpha=0.5, zorder = 5, marker = 'None',
                    linestyle = 'solid', linewidth = 3)
    ax.set_ylabel("Time [s]")
    ax.set_yscale('log')
    ax.set_title(f"Scaling")
    
    ax = fig.add_subplot(gs[1, 0])
    for b in backends:
        qubits = np.array(list(data[b].keys()))
        for n in noises: 
            yval = list()
            for q in qubits:
                yval.append(data[b][q][n]['cpu']['usage'][0])
            yval = np.array(yval)
            ax.scatter(qubits, yval, 
                       alpha=0.5, zorder = 10, edgecolor = 'k', s = 150, 
                       label = f'{b}.noise-{n}', 
                       marker = markerset[n],
                      )
            ax.plot(qubits, yval, 
                    alpha=0.5, zorder = 5, marker = 'None',
                    linestyle = 'solid', linewidth = 3)

    ax.set_ylabel("Host CPU Usage [%]")

    ax = fig.add_subplot(gs[2, 0])
    for b in backends:
        qubits = np.array(list(data[b].keys()))
        for n in noises: 
            yval = list()
            for q in qubits:
                yval.append(data[b][q][n]['cpu']['mem'])
            yval = np.array(yval)
            ax.scatter(qubits, yval, 
                       alpha=0.5, zorder = 10, edgecolor = 'k', s = 150, 
                       label = f'{b}.noise-{n}', 
                      marker = markerset[n])
            ax.plot(qubits, yval, 
                    alpha=0.5, zorder = 5, marker = 'None',
                    linestyle = 'solid', linewidth = 3)
    ax.set_ylabel("Host Mem [GiB]")
    ax.set_yscale('log')

    ax = fig.add_subplot(gs[3, 0])
    for b in backends:
        qubits = np.array(list(data[b].keys()))
        for n in noises: 
            yval = list()
            for q in qubits:
                yval.append(data[b][q][n]['gpu']['usage'][0])
            yval = np.array(yval)
            ax.scatter(qubits, yval, 
                       alpha=0.5, zorder = 10, edgecolor = 'k', s = 150, 
                       label = f'{b}.noise-{n}', 
                      marker = markerset[n])
            ax.plot(qubits, yval, 
                    alpha=0.5, zorder = 5, marker = 'None',
                    linestyle = 'solid', linewidth = 3)
    ax.set_ylabel("GPU Usage [%]")

    ax = fig.add_subplot(gs[4, 0])
    for b in backends:
        qubits = np.array(list(data[b].keys()))
        for n in noises: 
            yval = list()
            for q in qubits:
                yval.append(data[b][q][n]['gpu']['mem'][0])
            yval = np.array(yval)
            ax.scatter(qubits, yval, 
                       alpha=0.5, zorder = 10, edgecolor = 'k', s = 150, 
                       label = f'{b}.noise-{n}', 
                      marker = markerset[n])
            ax.plot(qubits, yval, 
                    alpha=0.5, zorder = 5, marker = 'None',
                    linestyle = 'solid', linewidth = 3)
    ax.set_ylabel("GPU Memory Usage [%]")
    ax.set_xlabel("Qubits")

    ax.legend()
    plt.tight_layout()
    plt.show()

def CompareResults(profdata : dict, b1 : str, b2 : str, nqubits : List[int] = None, noise : str = '0.0') -> None: 
    display(Markdown(f'### Comparing results at a given qubit count for {b1} and {b2} at noise level {noise}'))
    # get allowed qubit comparisions 
    if nqubits == None:
        nqb1 = set(profdata[b1].keys())
        nqb2 = set(profdata[b2].keys())
        nqubits = list(nqb1 & nqb2)
    for q in nqubits:
        d1 = profdata[b1][q][noise]
        d2 = profdata[b2][q][noise]
        display(Markdown(f'#### For num_qubits = {q}, which has num_gates = {d1['gates']}'))
        keys = d1['cpu'].keys()
        for k in keys: 
            display(Markdown(f'field : *{k}*'))
            display(Markdown(f'CPU | {d1['cpu'][k]}, {d2['cpu'][k]}'))
            display(Markdown(f'GPU | {d1['gpu'][k]}, {d2['gpu'][k]}'))
        
# lets compare noise to no noise 
def CompareToNoiseResults(profdata : dict, b1 : str, nqubits : List[int] = None, ideal : str = '0.0') -> None: 
    display(Markdown(f'### Comparing noisy results to ideal at a given qubit count for {b1}'))
    for q in profdata[b1].keys():
        noises = list(profdata[b1][q].keys())
        noises.remove(ideal)
        display(Markdown(f'#### For num_qubits = {q}'))
        for n in noises: 
            d1 = profdata[b1][q][ideal]
            d2 = profdata[b1][q][n]
            display(Markdown(f'num_gates for nose levels [{ideal}, {n}]] = [{d1['gates']}, {d2['gates']}]'))
            keys = d1['cpu'].keys()
            for k in keys: 
                display(Markdown(f'field : *{k}*'))
                display(Markdown(f'CPU | {d1['cpu'][k]}, {d2['cpu'][k]}'))
                display(Markdown(f'GPU | {d1['gpu'][k]}, {d2['gpu'][k]}'))

import cudaq

from braket.jobs.environment_variables import get_job_device_arn, get_hyperparameters, get_job_name
from braket.jobs.metrics import log_metric
from braket.jobs import save_job_result

from typing import List

print("Run hybrid job:", get_job_name())
cost_fevs = 0

print("Load hyperparameters")
hyperparameters = get_hyperparameters()
print(hyperparameters)
n_shots = int(hyperparameters.get("n_shots", 100))
max_iterations = int(hyperparameters.get("max_iterations", 2))

device = get_job_device_arn()
print(f"Running on device {device}")
if device.startswith("local"):
    cudaq.set_target(device.split("/")[-1])
else:
    cudaq.set_target("braket", machine=device)
print(f"CUDA-Q backend: {cudaq.get_target().name}")
print(f"NVIDIA GPUs available on instance: {cudaq.num_available_gpus()}")


# Cost function such that its minimal value corresponds to the qubit being in the state |1>.
def cost(parameters: List[float]):
    global cost_fevs
    cost_fevs += 1

    rx_angle = float(parameters[0])
    ry_angle = float(parameters[1])

    kernel = cudaq.make_kernel()
    qubits = kernel.qalloc(1)
    kernel.rx(rx_angle, qubits[0])
    kernel.ry(ry_angle, qubits[0])
    kernel.mz(qubits)

    result = dict(cudaq.sample(kernel, shots_count=n_shots).items())
    expectation_value = (1. * result.get('0', 0.) - 1. * result.get('1', 0.)) / n_shots

    log_metric(metric_name='rx_angle', value=rx_angle, iteration_number=cost_fevs)
    log_metric(metric_name='ry_angle', value=ry_angle, iteration_number=cost_fevs)
    log_metric(metric_name='cost_value', value=expectation_value, iteration_number=cost_fevs)
    return expectation_value


print("Initial value of the cost function:")
initial_parameters = [0, 0]
cost(initial_parameters)

print("Minimization...")
optimizer = cudaq.optimizers.COBYLA()
optimizer.initial_parameters = initial_parameters
optimizer.max_iterations = max_iterations
result = optimizer.optimize(dimensions=2, function=cost)

print(result)
save_job_result(result)

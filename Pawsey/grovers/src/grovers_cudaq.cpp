// @brief Grover's algorithm using CUDA-Q C++
#include "grovers_cudaq.h"

constexpr std::array<void (*)(cudaq::qubit &), 3> pauli_ops = {
    cudaq::x, cudaq::y, cudaq::z};

// Generalized noisy gate template
template <void (*Gate)(cudaq::qubit &)>
__qpu__ void noisy_gate(cudaq::qview<> qubit, float depol_prob, float p1,
                        float p2) {

  Gate(qubit[0]); // Apply the main gate (X, Y, or Z)

  if (depol_prob > p1) { // Apply depolarizing noise conditionally
    int idx = static_cast<int>(p2 * 3) % 3;
    pauli_ops[idx](qubit[0]); // Apply random depolarizing noise
  }
}

// Define specific noisy versions of X, Y, and Z gates
__qpu__ void noisy_x(cudaq::qview<> qubit, float depol_prob, float p1,
                     float p2) {
  noisy_gate<cudaq::x>(qubit, depol_prob, p1, p2);
}

__qpu__ void noisy_y(cudaq::qview<> qubit, float depol_prob, float p1,
                     float p2) {
  noisy_gate<cudaq::y>(qubit, depol_prob, p1, p2);
}

__qpu__ void noisy_z(cudaq::qview<> qubit, float depol_prob, float p1,
                     float p2) {
  noisy_gate<cudaq::z>(qubit, depol_prob, p1, p2);
}

__qpu__ void noisy_h(cudaq::qview<> qubit, float depol_prob, float p1,
                     float p2) {
  noisy_gate<cudaq::h>(qubit, depol_prob, p1, p2);
}

// Apply depolarizing noise without a preceding gate
__qpu__ void depol_noise(cudaq::qview<> qubit, float depol_prob, float p1,
                         float p2) {
  if (depol_prob > p1) {
    int idx = static_cast<int>(p2 * 3) % 3;
    pauli_ops[idx](qubit[0]); // Apply random depolarizing noise
  }
}

// Here we go defining a kernel to operate on the kernel
struct kernel {
  auto operator()(const int n, const int namp) __qpu__ {

    auto qvector = cudaq::qvector(n);

    auto qcontrol = qvector.front(n - 1);
    auto &qtarget = qvector.back();

    // superposition
    cudaq::h(qvector);

    for (int i = 0; i < namp; i++) {
      // Mark state 010101...
      for (std::size_t k = 0; k < qvector.size(); k += 2) {
        cudaq::x(qvector[k]);
      }
      cudaq::z<cudaq::ctrl>(qcontrol, qtarget);
      for (std::size_t k = 0; k < qvector.size(); k += 2) {
        cudaq::x(qvector[k]);
      }

      // Diffusion Unitary
      cudaq::h(qvector);
      cudaq::x(qvector);
      cudaq::z<cudaq::ctrl>(qcontrol, qtarget);
      cudaq::x(qvector);
      cudaq::h(qvector);
    }
    cudaq::mz(qvector);
  }
};

struct noisy_kernel {
  auto operator()(const int n, const int namp, float depol_prob,
                  std::vector<float> depol_probs,
                  std::vector<float> gate_probs) __qpu__ {
    auto qvector = cudaq::qvector(n);

    auto qcontrol = qvector.front(n - 1);
    auto &qtarget = qvector.back();

    VectorIterator p1(depol_probs);
    VectorIterator p2(gate_probs);

    auto apply_noisy_qvector = [&](auto &&gate_func) {
      for (std::size_t k = 0; k < qvector.size(); k++) {
        gate_func(qvector.slice(k, 1), depol_prob, p1.next(), p2.next());
      }
    };

    auto apply_noisy_qubit = [&](auto &&gate_func, size_t k) {
      gate_func(qvector.slice(k, 1), depol_prob, p1.next(), p2.next());
    };

    // superposition
    apply_noisy_qvector(noisy_h);

    for (int i = 0; i < namp; i++) {
      // Mark state 010101...
      for (std::size_t k = 0; k < qvector.size(); k += 2) {
        apply_noisy_qubit(noisy_x, k);
      }
      cudaq::z<cudaq::ctrl>(qcontrol, qtarget);
      apply_noisy_qvector(depol_noise);
      for (std::size_t k = 0; k < qvector.size(); k += 2) {
        apply_noisy_qubit(noisy_x, k);
      }

      // Diffusion Unitary
      apply_noisy_qvector(noisy_h);
      apply_noisy_qvector(noisy_x);
      cudaq::z<cudaq::ctrl>(qcontrol, qtarget);
      apply_noisy_qvector(depol_noise);
      apply_noisy_qvector(noisy_x);
      apply_noisy_qvector(noisy_h);
    }
    cudaq::mz(qvector);
  }
};

template <typename Kernel, typename... Args>
int countKernelGates(Kernel &&kernel, Args &&...args) {
  cudaq::ExecutionContext context("tracer");
  auto &platform = cudaq::get_platform();
  platform.set_exec_ctx(&context);

  kernel(std::forward<Args>(args)...);

  platform.reset_exec_ctx();

  cudaq::Resources resources = cudaq::Resources::compute(context.kernelTrace);

  // Return counts of all gates, alternatively get counts for a particular gate
  // e.g. resources.count("h"), or see a summary of resource usage with
  // resources.dump()

  return resources.count();
}

// Count number of gates, including insertions due to simulation of depolarising
// noise
template <typename Kernel, typename NoisyKernel, typename Options>
std::size_t getGateCount(const Options &opt, NoiseProbGenerator prob_gen) {
  std::size_t total_count = 0;

  // If no depolarisation, count gates once and return
  if (opt.depol_prob == 0) {
    return countKernelGates(Kernel{}, opt.num_qubits, opt.num_amplification);
  }

  // Otherwise, average the number of iterations and shots
  for (auto i = 0; i < opt.num_iterations; i++) {
    for (auto j = 0; j < opt.num_trajectories; j++) {
      auto [depol_probs, gate_probs] = prob_gen.depol_and_gate_probs(opt);
      total_count +=
          countKernelGates(NoisyKernel{}, opt.num_qubits, opt.num_amplification,
                           opt.depol_prob, depol_probs, gate_probs);
    }
  }

  return total_count / opt.num_iterations;
}

void visualiseCircuit(const Options &opt, NoiseProbGenerator &prob_gen) {
  std::cout<<"Gate Count : "<<getGateCount<kernel, noisy_kernel>(opt, prob_gen) << std::endl;
  if (opt.depol_prob == 0) {
    std::cout << cudaq::draw(kernel{}, opt.num_qubits, opt.num_amplification);

  } else {
    auto [depol_probs, gate_probs] = prob_gen.depol_and_gate_probs(opt);
    std::cout << cudaq::draw(noisy_kernel{}, opt.num_qubits,
                             opt.num_amplification, opt.depol_prob, depol_probs,
                             gate_probs);
  }
}

/// @brief Run the quantum circuit
/// @param argc
/// @param argv
/// @return
int main(int argc, char **argv) {

  auto opt = GetArgs(argc, argv);

  NoiseProbGenerator prob_gen(42);

  if (opt.visualise) {
    visualiseCircuit(opt, prob_gen);
    return 0;
  }

  auto gate_count = getGateCount<kernel, noisy_kernel>(opt, prob_gen);

  Log() << " Running Grovers" << std::endl;
  LogParallelAPI();
  LogBinding();
  LogSystemMem();

  Log() << "Grovers run with :"
        << " num_qubits = " << opt.num_qubits
        << " num_amplifaction = " << opt.num_amplification
        << " num_shots = " << opt.num_shots 
        << " depol_prob = " << opt.depol_prob
        << " num_trajectories = " << opt.num_trajectories
        << " with timings and usage averaged over " << opt.num_iterations
	      << " iterations"
        << std::endl;

  Log() << " Number of gates in circuit = " << gate_count << std::endl;

  // Reset random number generator for consistency in gate count
  prob_gen.reset();

  // get some timers
  auto timer = NewTimer();
  auto sampler = NewComputeSampler(0.01);

  std::map<std::string, int> final_counts;

  // Timing just the sample execution.
  for (auto i = 0; i < opt.num_iterations; i++) {
    if (opt.depol_prob == 0) {
      auto result = cudaq::sample(opt.num_shots, kernel{}, opt.num_qubits,
                                  opt.num_amplification);
      if (i == opt.num_iterations - 1) {
        for (const auto &[bitstring, count] : result) {
          final_counts[bitstring] += count;
        }
      }
    } else {
      // To do a noisy simulation we need to average over multiple trajectories
      for (int j = 0; j < opt.num_trajectories; j++) {
        auto [depol_probs, gate_probs] = prob_gen.depol_and_gate_probs(opt);
        auto result = cudaq::sample(opt.num_shots, noisy_kernel{}, opt.num_qubits,
                                    opt.num_amplification, opt.depol_prob,
                                    depol_probs, gate_probs);
        for (const auto &[bitstring, count] : result) {
            final_counts[bitstring] += count;
        }
      }
    }
  }
  LogTimeTaken(timer);
#ifdef _GPU
  LogTimeTakenOnDevice(timer);
#endif
  LogCPUUsage(sampler);
  LogMemUsage();
#ifdef _GPU
  LogGPUStatistics(sampler);
#endif

  if (opt.output_filename != "") {
    writeCountsToFile(final_counts, opt.output_filename);
  }

  return 0;
}

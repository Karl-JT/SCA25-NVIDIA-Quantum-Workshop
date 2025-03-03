/// @file grovers_cudaq.h
/// @brief include file for non-quantum related functions

// lets include the relevant libraries
#include <array>
#include <cmath>
#include <fstream>
#include <iostream>
#include <map>
#include <random>
#include <string>
#include <vector>
// load cuda
#include <cudaq.h>
#include <cudaq/algorithm.h>
#include <cudaq/algorithms/draw.h>
#include <cudaq/algorithms/resource_estimation.h>
#include <cudaq/spin_op.h>
// load profiling utility
#include <profile_util.h>

/// @brief Options structure to store information about the quantum circuit
struct Options {
  int num_qubits = 10;
  int num_amplification = 10;
  int num_shots = 100;
  int num_iterations = 1;
  float depol_prob = 0;
  int num_trajectories = 1;
  bool visualise = false;
  std::string output_filename = "";
};

void usage() {
  Options opt;
  std::cout << "Usage : \n";
  std::cout << " -n <num_qubits [" << opt.num_qubits << "]>\n";
  std::cout << " -a <num_amplification [" << opt.num_amplification << "]>\n";
  std::cout << " -s <num_shots [" << opt.num_shots << "]>\n";
  std::cout << " -i <num_iterations [" << opt.num_iterations << "]>\n";
  std::cout << " -d <depolarising_gate_probability [" << opt.depol_prob << "]>\n";
  std::cout << " -t <num_trajectories [" << opt.num_trajectories << "]>\n";
  std::cout << " -o <output_filename >\n";
  std::cout << " -v visualise the circuit and exit\n";
  exit(0);
};

Options GetArgs(int argc, char **argv) {
  Options opt;
  for (;;) {
    switch (getopt(argc, argv, "n:a:s:i:d:vo:t:")) {
    case 'n':
      opt.num_qubits = atoi(optarg);
      continue;
    case 'a':
      opt.num_amplification = atoi(optarg);
      continue;
    case 's':
      opt.num_shots = atoi(optarg);
      continue;
    case 'i':
      opt.num_iterations = atoi(optarg);
      continue;
    case 'd':
      opt.depol_prob = atof(optarg);
      continue;
    case 'v':
      opt.visualise = true;
      continue;
    case 'o':
      opt.output_filename = optarg;
      continue;
    case 't':
      opt.num_trajectories = atoi(optarg);
      continue;
    case '?':
    case 'h':
    default:
      usage();
      break;
    case -1:
      break;
    }
    break;
  }
  return opt;
};

/// @brief Used to generate reproducible depolarising noise probabilities and
/// gate probabilities.
class NoiseProbGenerator {
public:
  NoiseProbGenerator(unsigned int seed) : initial_seed(seed), gen(seed) {}

  // Reset the generator to the initial seed.
  void reset() { gen.seed(initial_seed); }

  std::vector<float> generate(int N) {
    std::uniform_real_distribution<float> dist(0.0f, 1.0f);
    std::vector<float> randomValues(N);
    for (int i = 0; i < N; ++i) {
      randomValues[i] = dist(gen);
    }
    return randomValues;
  }

  /// @brief Generate two vectors of random floats for simulations with
  /// depolarising noise.
  std::pair<std::vector<float>, std::vector<float>>
  depol_and_gate_probs(const Options &opt) {
    int count = 2 * 10 * opt.num_qubits * opt.num_amplification;
    std::vector<float> depol_probs = generate(count);
    std::vector<float> gate_probs = generate(count);
    return {depol_probs, gate_probs};
  }

private:
  unsigned int initial_seed;
  std::mt19937 gen;
};

/// @brief A simple iterator class for std::vector<float>.
class VectorIterator {
private:
  std::vector<float>::const_iterator current;
  std::vector<float>::const_iterator end;

public:
  explicit VectorIterator(const std::vector<float> &vec)
      : current(vec.begin()), end(vec.end()) {}
  float next() {
    if (current == end) {
      throw std::out_of_range("No more elements");
    }
    return *current++;
  }
  bool hasNext() const { return current != end; }
  void reset() { current = end - std::distance(current, end); }
};

/// @brief write bitstring counts to file
void writeCountsToFile(const std::map<std::string, int> &counts,
                       const std::string &output_filename) {
  std::ofstream out_file(output_filename);
  if (!out_file.is_open()) {
    std::cerr << "Error: Could not open " << output_filename << " for writing."
              << std::endl;
    return;
  }
  for (const auto &[bitstring, count] : counts) {
    out_file << bitstring << " : " << count << "\n";
  }
  out_file.close();
}

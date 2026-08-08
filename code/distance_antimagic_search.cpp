#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <random>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

namespace {
constexpr int kMaxN = 10;
using Adjacency = std::array<std::uint16_t, kMaxN>;
using Permutation = std::array<int, kMaxN>;
using Weights = std::array<int, kMaxN>;

int graph6_order(const std::string& s) {
    if (s.empty()) throw std::runtime_error("Empty graph6 line");
    const unsigned char c = static_cast<unsigned char>(s[0]);
    if (c == '~') throw std::runtime_error("Extended graph6 headers are not supported");
    const int n = static_cast<int>(c) - 63;
    if (n < 1 || n > kMaxN) throw std::runtime_error("Supported graph order is 1..10");
    return n;
}

Adjacency decode_graph6(const std::string& s, int n) {
    const int edge_bits = n * (n - 1) / 2;
    const int needed_chars = 1 + (edge_bits + 5) / 6;
    if (static_cast<int>(s.size()) < needed_chars) {
        throw std::runtime_error("Truncated graph6 record: " + s);
    }

    Adjacency adj{};
    int bitpos = 0;
    for (int j = 1; j < n; ++j) {
        for (int i = 0; i < j; ++i) {
            const int char_index = 1 + bitpos / 6;
            const int within = bitpos % 6;
            const int value = static_cast<int>(static_cast<unsigned char>(s[char_index])) - 63;
            if (value < 0 || value > 63) throw std::runtime_error("Invalid graph6 character");
            const int bit = (value >> (5 - within)) & 1;
            if (bit) {
                adj[i] |= static_cast<std::uint16_t>(1u << j);
                adj[j] |= static_cast<std::uint16_t>(1u << i);
            }
            ++bitpos;
        }
    }
    return adj;
}

bool has_distinct_open_neighborhoods(const Adjacency& adj, int n) {
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            if (adj[i] == adj[j]) return false;
        }
    }
    return true;
}

int edge_count(const Adjacency& adj, int n) {
    int degree_sum = 0;
    for (int i = 0; i < n; ++i) {
        degree_sum += __builtin_popcount(static_cast<unsigned>(adj[i]));
    }
    return degree_sum / 2;
}

bool verify_labeling(const Adjacency& adj, int n, const Permutation& labels,
                     Weights* out_weights = nullptr) {
    std::uint64_t seen = 0;
    Weights weights{};
    for (int v = 0; v < n; ++v) {
        unsigned mask = adj[v];
        int sum = 0;
        while (mask != 0) {
            const unsigned u = static_cast<unsigned>(__builtin_ctz(mask));
            sum += labels[u];
            mask &= mask - 1;
        }
        weights[v] = sum;
        const std::uint64_t flag = std::uint64_t{1} << sum;
        if ((seen & flag) != 0) return false;
        seen |= flag;
    }
    if (out_weights != nullptr) *out_weights = weights;
    return true;
}

template <typename ArrayType>
std::string join_values(const ArrayType& values, int n) {
    std::ostringstream out;
    for (int i = 0; i < n; ++i) {
        if (i) out << ',';
        out << values[i];
    }
    return out.str();
}

struct EdgeStats {
    std::uint64_t total = 0;
    std::uint64_t point_determining = 0;
    std::uint64_t attempts = 0;
    std::uint64_t fallback = 0;
    std::uint64_t max_attempt = 0;
};
}  // namespace

int main(int argc, char** argv) {
    if (argc < 3) {
        std::cerr << "Usage: " << argv[0]
                  << " input.g6 output_prefix [seed=20260807] [pool=20000]\n";
        return 2;
    }

    const std::string input_path = argv[1];
    const std::string output_prefix = argv[2];
    const std::uint64_t seed = argc >= 4 ? std::stoull(argv[3]) : 20260807ULL;
    std::size_t pool_size = argc >= 5 ? std::stoull(argv[4]) : 20000ULL;

    std::ifstream input(input_path);
    if (!input) {
        std::cerr << "Cannot open input: " << input_path << '\n';
        return 2;
    }

    std::string first_record;
    while (std::getline(input, first_record)) {
        if (!first_record.empty() && first_record.back() == '\r') first_record.pop_back();
        if (!first_record.empty() && first_record[0] != '>') break;
    }
    if (first_record.empty()) {
        std::cerr << "No graph6 records found\n";
        return 2;
    }
    const int n = graph6_order(first_record);
    input.clear();
    input.seekg(0);

    std::vector<Permutation> permutations;
    Permutation current{};
    for (int i = 0; i < n; ++i) current[i] = i + 1;
    do {
        permutations.push_back(current);
    } while (std::next_permutation(current.begin(), current.begin() + n));

    std::mt19937_64 rng(seed);
    std::shuffle(permutations.begin(), permutations.end(), rng);
    pool_size = std::min(pool_size, permutations.size());

    const int mask_count = 1 << n;
    std::vector<std::vector<std::uint8_t>> pool_sums(
        pool_size, std::vector<std::uint8_t>(mask_count, 0));
    for (std::size_t k = 0; k < pool_size; ++k) {
        for (int mask = 1; mask < mask_count; ++mask) {
            const int bit = __builtin_ctz(static_cast<unsigned>(mask));
            pool_sums[k][mask] = static_cast<std::uint8_t>(
                pool_sums[k][mask & (mask - 1)] + permutations[k][bit]);
        }
    }

    std::ofstream certificates(output_prefix + "_certificates.tsv");
    std::ofstream hard_cases(output_prefix + "_hard_cases.tsv");
    if (!certificates || !hard_cases) {
        std::cerr << "Cannot create output files\n";
        return 2;
    }
    const std::string header =
        "index\tgraph6\tedges\tsearch_rank\tlabels_v0_to_vn_minus_1\tweights_v0_to_vn_minus_1\n";
    certificates << header;
    hard_cases << header;

    const int max_edges = n * (n - 1) / 2;
    std::vector<EdgeStats> edge_stats(max_edges + 1);
    std::unordered_map<std::uint64_t, std::uint64_t> rank_histogram;

    std::uint64_t total = 0;
    std::uint64_t point_determining = 0;
    std::uint64_t repeated_neighborhood = 0;
    std::uint64_t fallback_count = 0;
    std::uint64_t failed = 0;
    std::uint64_t global_max_rank = 0;
    std::string max_graph6;
    int max_graph_edges = 0;
    Permutation max_labels{};
    Weights max_weights{};

    const auto start = std::chrono::steady_clock::now();
    std::string line;
    while (std::getline(input, line)) {
        if (!line.empty() && line.back() == '\r') line.pop_back();
        if (line.empty() || line[0] == '>') continue;
        ++total;

        if (graph6_order(line) != n) {
            std::cerr << "Mixed graph orders at record " << total << '\n';
            return 3;
        }
        const Adjacency adj = decode_graph6(line, n);
        const int edges = edge_count(adj, n);
        edge_stats[edges].total++;

        if (!has_distinct_open_neighborhoods(adj, n)) {
            ++repeated_neighborhood;
            continue;
        }
        ++point_determining;
        edge_stats[edges].point_determining++;

        bool found = false;
        std::uint64_t rank = 0;
        Permutation witness{};
        Weights weights{};

        for (std::size_t k = 0; k < pool_size; ++k) {
            std::uint64_t seen = 0;
            bool valid = true;
            for (int v = 0; v < n; ++v) {
                const int weight = pool_sums[k][adj[v]];
                const std::uint64_t flag = std::uint64_t{1} << weight;
                if ((seen & flag) != 0) {
                    valid = false;
                    break;
                }
                seen |= flag;
                weights[v] = weight;
            }
            if (valid) {
                found = true;
                rank = k + 1;
                witness = permutations[k];
                break;
            }
        }

        if (!found) {
            ++fallback_count;
            edge_stats[edges].fallback++;
            for (std::size_t k = pool_size; k < permutations.size(); ++k) {
                if (verify_labeling(adj, n, permutations[k], &weights)) {
                    found = true;
                    rank = k + 1;
                    witness = permutations[k];
                    break;
                }
            }
        }

        if (!found) {
            ++failed;
            std::cerr << "NO WITNESS: index=" << total << " graph6=" << line << '\n';
            continue;
        }

        Weights direct_weights{};
        if (!verify_labeling(adj, n, witness, &direct_weights) || direct_weights != weights) {
            std::cerr << "Internal verification failure at record " << total << '\n';
            return 4;
        }

        edge_stats[edges].attempts += rank;
        edge_stats[edges].max_attempt = std::max(edge_stats[edges].max_attempt, rank);
        rank_histogram[rank]++;
        if (rank > global_max_rank) {
            global_max_rank = rank;
            max_graph6 = line;
            max_graph_edges = edges;
            max_labels = witness;
            max_weights = weights;
        }

        certificates << total << '\t' << line << '\t' << edges << '\t' << rank << '\t'
                     << join_values(witness, n) << '\t' << join_values(weights, n) << '\n';
        if (rank > 1000) {
            hard_cases << total << '\t' << line << '\t' << edges << '\t' << rank << '\t'
                       << join_values(witness, n) << '\t' << join_values(weights, n) << '\n';
        }
    }
    certificates.close();
    hard_cases.close();

    const double elapsed = std::chrono::duration<double>(
        std::chrono::steady_clock::now() - start).count();

    std::ofstream summary(output_prefix + "_summary.txt");
    summary << "input=" << input_path << '\n'
            << "order=" << n << '\n'
            << "seed=" << seed << '\n'
            << "permutations=" << permutations.size() << '\n'
            << "pool_size=" << pool_size << '\n'
            << "total_graphs=" << total << '\n'
            << "distinct_neighborhood_graphs=" << point_determining << '\n'
            << "repeated_neighborhood_graphs=" << repeated_neighborhood << '\n'
            << "witnesses_found=" << (point_determining - failed) << '\n'
            << "failed=" << failed << '\n'
            << "fallback_count=" << fallback_count << '\n'
            << "max_search_rank=" << global_max_rank << '\n'
            << "max_case_graph6=" << max_graph6 << '\n'
            << "max_case_edges=" << max_graph_edges << '\n'
            << "max_case_labels=" << join_values(max_labels, n) << '\n'
            << "max_case_weights=" << join_values(max_weights, n) << '\n'
            << "elapsed_seconds=" << std::fixed << std::setprecision(6) << elapsed << '\n';

    std::ofstream edge_output(output_prefix + "_by_edges.csv");
    edge_output << "edges,total_graphs,distinct_neighborhood_graphs,repeated_neighborhood_graphs,"
                   "mean_search_rank,max_search_rank,fallback_count\n";
    for (int edges = 0; edges <= max_edges; ++edges) {
        const EdgeStats& s = edge_stats[edges];
        if (s.total == 0) continue;
        const double mean_rank = s.point_determining == 0
                                     ? 0.0
                                     : static_cast<double>(s.attempts) / static_cast<double>(s.point_determining);
        edge_output << edges << ',' << s.total << ',' << s.point_determining << ','
                    << (s.total - s.point_determining) << ',' << std::fixed
                    << std::setprecision(6) << mean_rank << ',' << s.max_attempt << ','
                    << s.fallback << '\n';
    }

    std::vector<std::pair<std::uint64_t, std::uint64_t>> histogram(
        rank_histogram.begin(), rank_histogram.end());
    std::sort(histogram.begin(), histogram.end());
    std::ofstream histogram_output(output_prefix + "_attempt_histogram.csv");
    histogram_output << "search_rank,count\n";
    for (const auto& [rank, count] : histogram) histogram_output << rank << ',' << count << '\n';

    std::cout << "order=" << n << " total=" << total
              << " point_determining=" << point_determining
              << " repeated_neighborhood=" << repeated_neighborhood
              << " failed=" << failed << " fallback=" << fallback_count
              << " max_rank=" << global_max_rank << " elapsed=" << elapsed << "s\n";
    return failed == 0 ? 0 : 1;
}

import argparse

def load_reference_genome(reference_file):
    """
    Load the reference genome from a file.
    This function assumes a simple format where each line represents a sequence of a chromosome or contig.
    Adjust this function based on the actual format of your reference genome.
    """
    with open(reference_file, 'r') as file:
        return {line.strip().split()[0]: line.strip().split()[1] for line in file}

def process_coverage_file(coverage_file, depth_threshold):
    """
    Process the coverage file to identify positions with coverage below the specified threshold.
    """
    coverage_data = {}
    with open(coverage_file, 'r') as file:
        for line in file:
            parts = line.strip().split()
            ref_name, pos, depth = parts[0], int(parts[1]), int(parts[2])
            if depth < depth_threshold:
                if ref_name not in coverage_data:
                    coverage_data[ref_name] = []
                coverage_data[ref_name].append(pos)
    return coverage_data

def generate_consensus(reference_genome, coverage_data):
    """
    Generate the consensus sequence, marking positions with low coverage as 'N'.
    """
    consensus_genome = {}
    for ref_name, seq in reference_genome.items():
        consensus_seq = list(seq)  # Convert string to list for mutability
        for pos in coverage_data.get(ref_name, []):
            consensus_seq[pos-1] = "N"  # Adjust for 0-based indexing
        consensus_genome[ref_name] = ''.join(consensus_seq)
    return consensus_genome

def write_consensus_genome(consensus_genome, output_file):
    """
    Write the consensus genome to an output file.
    """
    with open(output_file, 'w') as file:
        for ref_name, seq in consensus_genome.items():
            file.write(f">{ref_name}\n{seq}\n")

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Generate a consensus genome with 'N' for low-coverage positions.")
    parser.add_argument("--reference", required=True, help="Path to the reference genome file")
    parser.add_argument("--coverage_file", required=True, help="Path to the coverage file")
    parser.add_argument("--output_file", required=True, help="Path to the output consensus genome file")
    parser.add_argument("--depth_threshold", type=int, default=10, help="Coverage depth threshold below which bases are marked as 'N'")
    args = parser.parse_args()

    # Load the reference genome
    reference_genome = load_reference_genome(args.reference)

    # Process the coverage file
    coverage_data = process_coverage_file(args.coverage_file, args.depth_threshold)

    # Generate the consensus genome
    consensus_genome = generate_consensus(reference_genome, coverage_data)

    # Write the consensus genome to the output file
    write_consensus_genome(consensus_genome, args.output_file)

    print(f"Consensus genome generated and saved to {args.output_file}")

if __name__ == "__main__":
    main()

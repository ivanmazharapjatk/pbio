import random

def get_custom_distribution() -> list:
    """Gets and validates a custom nucleotide probability distribution."""
    while True:
        try:
            print("\nSet nucleotide distribution (must sum to 100%):")
            p_a = float(input("  A (%): "))
            p_c = float(input("  C (%): "))
            p_g = float(input("  G (%): "))
            p_t = float(input("  T (%): "))

            total = p_a + p_c + p_g + p_t

            if abs(total - 100.0) < 1e-6:
                return [p_a, p_c, p_g, p_t]
            else:
                print(f"Error: Probabilities sum to {total:.2f}%, not 100%. Try again.")
        except ValueError:
            print("Error: Please enter numeric values.")

def generate_sequence(length: int, weights: list = None) -> str:
    """Returns a random DNA sequence of the specified length using given weights."""
    nucleotides = ['A', 'C', 'G', 'T']
    if weights is None:
        weights = [25, 25, 25, 25] # Default distribution
    return ''.join(random.choices(nucleotides, weights=weights, k=length))

def calculate_stats(sequence: str) -> dict:
    """Returns a dictionary of sequence statistics.
Keys: "A", "C", "G", "T" ( float values , %),
           "GC" ( float value , %)."""
    n = len(sequence)

    if n == 0:
        return {"A": 0.0, "C": 0.0, "G": 0.0, "T": 0.0, "gc_ratio_A": 0.0}

    return {
        "A": (sequence.count('A') / n) * 100,
        "C": (sequence.count('C') / n) * 100,
        "G": (sequence.count('G') / n) * 100,
        "T": (sequence.count('T') / n) * 100,
        "gc_ratio_A": ((sequence.count('G') + sequence.count('C')) / n) * 100
    }

def insert_name(sequence: str, name: str) -> str:
    """Inserts a name at a random position in the sequence.
Name written in lowercase letters."""
    name_lower = name.lower()
    insert_pos = random.randint(0, len(sequence))
    return sequence[:insert_pos] + name_lower + sequence[insert_pos:]


def format_fasta(seq_id: str , description: str ,
                 sequence: str, line_width: int = 80) -> str:
    """Returns a formatted FASTA record as a string."""
    header = f">{seq_id} {description}".strip()
    lines = [header]

    for i in range(0, len(sequence), line_width):
        lines.append(sequence[i:i + line_width])

    fasta_string = "\n".join(lines)
    fasta_string += "\n\n# EOF_1"

    return fasta_string

def validate_positive_int(prompt: str,
                          min_val: int = 1,
                          max_val: int = 100_000) -> int:
    """Gets an integer from the user in a range.
In case of an error, repeats the question."""
    while True:
        try:
            value = int(input(prompt))
            if min_val <= value <= max_val:
                return value
            else:
                print(f"Error: value must be an integer in the range [{min_val}, {max_val}].")
        except ValueError:
            print(f"Error: value must be an integer in the range [{min_val}, {max_val}].")

def find_motif(sequence: str, motif: str) -> list:
    """Returns a list of 1-based indices where the motif occurs."""
    if not motif:
        return []
    motif = motif.upper()
    return [i + 1 for i in range(len(sequence) - len(motif) + 1) if sequence[i:i+len(motif)] == motif]

def get_complement(sequence: str) -> str:
    """Generates the complementary DNA strand (A->T, C->G)."""
    comp_map = str.maketrans('ACGT', 'TGCA')
    return sequence.upper().translate(comp_map)

def get_reverse_complement(sequence: str) -> str:
    """Generates the reverse complementary DNA strand."""
    return get_complement(sequence)[::-1]

def main():
    """Main execution block."""
    print("--- DNA Sequence Generator ---")
    num_sequences = validate_positive_int("Enter number of sequences to generate (batch size): ", 1, 1000)
    length = validate_positive_int("Enter sequence length: ")

    while True:
        base_id = input("Enter base sequence ID: ")
        if not base_id:
            print("Error: ID cannot be empty.")
        elif any(char.isspace() for char in base_id):
            print("Error: ID cannot contain whitespace.")
        else:
            break

    description = input("Enter a description of the sequence(s): ")
    name = input("Enter your name (for the insertion challenge): ")
    weights = get_custom_distribution()
    motif = input("\nEnter a motif to search for (e.g., 'ATG', or leave blank to skip): ").strip()

    fasta_records = []

    print("\n--- Generation Results ---")
    for i in range(1, num_sequences + 1):
        seq_id = f"{base_id}_{i:03d}" if num_sequences > 1 else base_id

        pure_sequence = generate_sequence(length, weights)
        stats = calculate_stats(pure_sequence)

        comp_sequence = get_complement(pure_sequence)
        rev_comp_sequence = get_reverse_complement(pure_sequence)

        motif_positions = find_motif(pure_sequence, motif)

        print(f"\n[ Record: {seq_id} ]")
        print(f"GC-content: {stats['gc_ratio_A']:.2f}%")
        if motif:
            if motif_positions:
                print(f"Motif '{motif.upper()}' found at positions: {motif_positions}")
            else:
                print(f"Motif '{motif.upper()}' not found.")

        final_main = insert_name(pure_sequence, name)
        final_comp = insert_name(comp_sequence, name)
        final_revcomp = insert_name(rev_comp_sequence, name)

        fasta_records.append(format_fasta(seq_id, description, final_main))
        fasta_records.append(format_fasta(f"{seq_id}_comp", f"Complementary strand of {seq_id}", final_comp))
        fasta_records.append(
            format_fasta(f"{seq_id}_revcomp", f"Reverse-complementary strand of {seq_id}", final_revcomp))

    final_fasta_output = "\n\n".join(fasta_records)
    final_fasta_output += "\n\n# EOF_1"

    file_name = f"{base_id}_batch.fasta" if num_sequences > 1 else f"{base_id}.fasta"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(final_fasta_output)

    print(f"\n>>> Saved {num_sequences * 3} total records (including complementary strands) to '{file_name}'")

if __name__ == "__main__":
    main()

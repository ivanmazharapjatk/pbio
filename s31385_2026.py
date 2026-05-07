import random

def generate_sequence(length: int) -> str:
    """Returns a random DNA sequence of the specified length."""
    nucleotides = ['A', 'C', 'G', 'T']
    return ''.join(random.choices(nucleotides, k=length))

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

def main():
    return

if __name__ == "__main__":
    main()

def generate_sequence(length: int) -> str:
    """Returns a random DNA sequence of the specified length."""

def calculate_stats(sequence: str) -> dict:
    """Returns a dictionary of sequence statistics.
Keys: "A", "C", "G", "T" ( float values , %),
           "GC" ( float value , %)."""

def insert_name(sequence: str, name: str) -> str:
    """Inserts a name at a random position in the sequence.
Name written in lowercase letters."""

def format_fasta(seq_id: str , description: str ,
                 sequence: str, line_width: int = 80) -> str:
    """Returns a formatted FASTA record as a string."""

def validate_positive_int(prompt: str,
                          min_val: int = 1,
                          max_val: int = 100_000) -> int:
    """Gets an integer from the user in a range.
In case of an error, repeats the question."""

def main():
    return

if __name__ == "__main__":
    main()

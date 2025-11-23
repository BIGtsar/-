import argparse
import sys

def create_codon_table():
    """Создает таблицу кодонов RNA -> аминокислот"""
    codon_table = {
        'UUU': 'F', 'UUC': 'F', 'UUA': 'L', 'UUG': 'L',
        'CUU': 'L', 'CUC': 'L', 'CUA': 'L', 'CUG': 'L',
        'AUU': 'I', 'AUC': 'I', 'AUA': 'I', 'AUG': 'M',
        'GUU': 'V', 'GUC': 'V', 'GUA': 'V', 'GUG': 'V',
        'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S',
        'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
        'ACU': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
        'GCU': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
        'UAU': 'Y', 'UAC': 'Y', 'UAA': '*', 'UAG': '*',
        'CAU': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
        'AAU': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
        'GAU': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
        'UGU': 'C', 'UGC': 'C', 'UGA': '*', 'UGG': 'W',
        'CGU': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
        'AGU': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
        'GGU': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G'
    }
    return codon_table

def rna_to_protein(rna_string):
    """Транслирует RNA строку в белковую последовательность"""
    codon_table = create_codon_table()
    protein = ""
    
    # Обрабатываем по 3 нуклеотида (кодоны)
    for i in range(0, len(rna_string) - 2, 3):
        codon = rna_string[i:i+3]
        amino_acid = codon_table.get(codon, '')
        
        # Останавливаемся на стоп-кодоне
        if amino_acid == '*':
            break
        
        protein += amino_acid
    
    return protein

def main():
    """Основная функция с интерфейсом командной строки"""
    parser = argparse.ArgumentParser(
        description='Translate RNA sequence to protein sequence',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python rna_to_protein.py -s "AUGGCCAUGGCGCCCAGAACUGAGAUCAAUAGUACCCGUAUUAACGGGUGA"
  python rna_to_protein.py -i input.txt -o output.txt
  python rna_to_protein.py < input.txt
        '''
    )
    
    # Группа для взаимно исключающих опций ввода
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-s', '--string', help='RNA string directly from command line')
    input_group.add_argument('-i', '--input', help='Input file containing RNA string')
    
    parser.add_argument('-o', '--output', help='Output file (optional)')
    
    args = parser.parse_args()
    
    # Чтение RNA строки
    if args.string:
        rna_sequence = args.string.upper().replace('T', 'U')  # Конвертируем DNA в RNA если нужно
    elif args.input:
        try:
            with open(args.input, 'r') as f:
                rna_sequence = f.read().strip().upper().replace('T', 'U')
        except FileNotFoundError:
            print(f"Error: File '{args.input}' not found.", file=sys.stderr)
            sys.exit(1)
    else:
        # Чтение из stdin
        rna_sequence = sys.stdin.read().strip().upper().replace('T', 'U')
    
    # Проверка валидности RNA строки
    valid_nucleotides = set('ACGU')
    if not all(nuc in valid_nucleotides for nuc in rna_sequence):
        print("Error: Invalid characters in RNA sequence. Only A, C, G, U allowed.", file=sys.stderr)
        sys.exit(1)
    
    # Трансляция в белок
    try:
        protein_sequence = rna_to_protein(rna_sequence)
    except Exception as e:
        print(f"Error during translation: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Вывод результата
    if args.output:
        with open(args.output, 'w') as f:
            f.write(protein_sequence + '\n')
        print(f"Protein sequence written to {args.output}")
    else:
        print(protein_sequence)

if name == "__main__":
    main()

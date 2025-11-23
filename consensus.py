import argparse
import sys
from collections import defaultdict

def parse_fasta(data):
    """Парсинг FASTA формата"""
    sequences = []
    current_seq = ""
    
    for line in data:
        line = line.strip()
        if line.startswith('>'):
            if current_seq:
                sequences.append(current_seq)
                current_seq = ""
        else:
            current_seq += line
    
    if current_seq:
        sequences.append(current_seq)
    
    return sequences

def calculate_profile_and_consensus(sequences):
    """Вычисление профильной матрицы и консенсусной строки"""
    if not sequences:
        return "", {}
    
    n = len(sequences[0])  # длина последовательностей
    
    # Проверяем, что все последовательности одинаковой длины
    for seq in sequences:
        if len(seq) != n:
            raise ValueError("All sequences must have the same length")
    
    # Инициализация профильной матрицы
    profile = {
        'A': [0] * n,
        'C': [0] * n, 
        'G': [0] * n,
        'T': [0] * n
    }
    
    # Заполнение профильной матрицы
    for seq in sequences:
        for i, nucleotide in enumerate(seq):
            if nucleotide not in profile:
                raise ValueError(f"Invalid nucleotide '{nucleotide}' in sequence")
            profile[nucleotide][i] += 1
    
    # Построение консенсусной строки
    consensus = ""
    for i in range(n):
        max_count = -1
        max_nucleotide = 'A'
        
        for nucleotide in ['A', 'C', 'G', 'T']:
            if profile[nucleotide][i] > max_count:
                max_count = profile[nucleotide][i]
                max_nucleotide = nucleotide
        
        consensus += max_nucleotide
    
    return consensus, profile

def main():
    """Основная функция с интерфейсом командной строки"""
    parser = argparse.ArgumentParser(
        description='Calculate consensus string and profile matrix from DNA sequences in FASTA format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python consensus_profile.py -i sequences.fasta
  python consensus_profile.py -i sequences.fasta -o result.txt
  python consensus_profile.py < sequences.fasta
        '''
    )
    
    parser.add_argument('-i', '--input', required=True, help='Input FASTA file')
    parser.add_argument('-o', '--output', help='Output file (optional)')
    
    args = parser.parse_args()
    
    try:
        # Чтение FASTA файла
        with open(args.input, 'r') as f:
            data = f.readlines()
        
        # Парсинг последовательностей
        sequences = parse_fasta(data)
        
        if not sequences:
            print("Error: No sequences found in FASTA file", file=sys.stderr)
            sys.exit(1)
        
        # Вычисление профиля и консенсуса
        consensus, profile = calculate_profile_and_consensus(sequences)
        
        # Формирование результата
        result_lines = []
        result_lines.append(consensus)
        result_lines.append(f"A: {' '.join(map(str, profile['A']))}")
        result_lines.append(f"C: {' '.join(map(str, profile['C']))}")
        result_lines.append(f"G: {' '.join(map(str, profile['G']))}")
        result_lines.append(f"T: {' '.join(map(str, profile['T']))}")
        
        result = '\n'.join(result_lines)
        
        # Вывод результата
        if args.output:
            with open(args.output, 'w') as f:
                f.write(result + '\n')
            print(f"Results written to {args.output}")
        else:
            print(result)
            
    except FileNotFoundError:
        print(f"Error: File '{args.input}' not found.", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

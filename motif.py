import argparse
import sys

def find_substring_positions(s, t):
    """
    Находит все начальные позиции подстроки t в строке s
    Позиции считаются с 1 (как в биологии)
    """
    positions = []
    pattern_length = len(t)
    
    for i in range(len(s) - pattern_length + 1):
        if s[i:i + pattern_length] == t:
            positions.append(i + 1)  # +1 для 1-based индексации
    
    return positions

def main():
    """Основная функция с интерфейсом командной строки"""
    parser = argparse.ArgumentParser(
        description='Find all locations of substring t in DNA string s',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python substring_locations.py -s "GATATATGCATATACTT" -t "ATAT"
  python substring_locations.py -i input.txt
  echo -e "GATATATGCATATACTT\\\\nATAT" | python substring_locations.py
        '''
    )
    
    # Группа для взаимно исключающих опций ввода
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-s', '--string', nargs=2, metavar=('S', 'T'), 
                           help='DNA strings s and t directly from command line')
    input_group.add_argument('-i', '--input', help='Input file containing two DNA strings')
    
    parser.add_argument('-o', '--output', help='Output file (optional)')
    
    args = parser.parse_args()
    
    # Чтение входных данных
    if args.string:
        s, t = args.string
    elif args.input:
        try:
            with open(args.input, 'r') as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
            if len(lines) < 2:
                print("Error: Input file must contain at least 2 lines", file=sys.stderr)
                sys.exit(1)
            s, t = lines[0], lines[1]
        except FileNotFoundError:
            print(f"Error: File '{args.input}' not found.", file=sys.stderr)
            sys.exit(1)
    else:
        # Чтение из stdin
        lines = [line.strip() for line in sys.stdin if line.strip()]
        if len(lines) < 2:
            print("Error: Need 2 DNA strings from stdin", file=sys.stderr)
            sys.exit(1)
        s, t = lines[0], lines[1]
    
    # Проверка валидности DNA строк
    valid_nucleotides = set('ACGT')
    if not all(nuc in valid_nucleotides for nuc in s):
        print("Error: Invalid characters in DNA string s. Only A, C, G, T allowed.", file=sys.stderr)
        sys.exit(1)
    if not all(nuc in valid_nucleotides for nuc in t):
        print("Error: Invalid characters in DNA string t. Only A, C, G, T allowed.", file=sys.stderr)
        sys.exit(1)
    
    if len(t) > len(s):
        print("Error: Substring t cannot be longer than string s", file=sys.stderr)
        sys.exit(1)
    
    # Поиск позиций
    try:
        positions = find_substring_positions(s, t)
    except Exception as e:
        print(f"Error during search: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Форматирование результата
    result = ' '.join(map(str, positions))
    
    # Вывод результата
    if args.output:
        with open(args.output, 'w') as f:
            f.write(result + '\n')
        print(f"Positions written to {args.output}")
    else:
        print(result)

if __name__ == "__main__":
    main()

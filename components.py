import argparse
import sys
from collections import defaultdict, deque

def dfs(node, visited, graph):
    """Обход в глубину для одной компоненты связности"""
    stack = [node]
    visited[node] = True
    
    while stack:
        current = stack.pop()
        for neighbor in graph[current]:
            if not visited[neighbor]:
                visited[neighbor] = True
                stack.append(neighbor)

def bfs(node, visited, graph):
    """Обход в ширину для одной компоненты связности"""
    queue = deque([node])
    visited[node] = True
    
    while queue:
        current = queue.popleft()
        for neighbor in graph[current]:
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append(neighbor)

def count_connected_components(n, edges, use_bfs=False):
    """Подсчет количества компонент связности в графе"""
    # Построение списка смежности
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    # Инициализация массива посещенных вершин
    visited = [False] * (n + 1)  # индексация с 1 до n
    components = 0
    
    # Обход всех вершин
    for i in range(1, n + 1):
        if not visited[i]:
            components += 1
            if use_bfs:
                bfs(i, visited, graph)
            else:
                dfs(i, visited, graph)
    
    return components

def main():
    """Основная функция с интерфейсом командной строки"""
    parser = argparse.ArgumentParser(
        description='Count connected components in an undirected graph using DFS/BFS',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python connected_components.py -i graph.txt
  python connected_components.py -i graph.txt --bfs
  python connected_components.py -i graph.txt -o result.txt
        '''
    )
    
    parser.add_argument('-i', '--input', required=True, help='Input file in edge list format')
    parser.add_argument('-o', '--output', help='Output file (optional)')
    parser.add_argument('--bfs', action='store_true', help='Use BFS instead of DFS')
    
    args = parser.parse_args()
    
    try:
        # Чтение входного файла
        with open(args.input, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        
        if not lines:
            print("Error: Input file is empty", file=sys.stderr)
            sys.exit(1)
        
        # Парсинг первой строки (количество вершин и ребер)
        first_line = lines[0].split()
        if len(first_line) < 2:
            print("Error: First line must contain n and m", file=sys.stderr)
            sys.exit(1)
        
        n = int(first_line[0])  # количество вершин
        m = int(first_line[1])  # количество ребер
        
        # Парсинг ребер
        edges = []
        for i in range(1, min(m + 1, len(lines))):
            line_parts = lines[i].split()
            if len(line_parts) >= 2:
                u = int(line_parts[0])
                v = int(line_parts[1])
                edges.append((u, v))
        
        # Подсчет компонент связности
        components = count_connected_components(n, edges, args.bfs)
        
        # Вывод результата
        result = str(components)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(result + '\n')
            print(f"Number of connected components: {components}")
            print(f"Result written to {args.output}")
        else:
            print(result)
            
    except FileNotFoundError:
        print(f"Error: File '{args.input}' not found.", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: Invalid data format - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

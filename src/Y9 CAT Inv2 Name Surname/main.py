def read_file(file):
    with open(file, 'r') as f:
        entries = f.read().splitlines()
    return entries

def return_longest_and_shortest_names(file):
    entries = read_file(file)

    if not entries:
        return 'The file is empty.'

    max_length = max(len(name) for name in entries)
    min_length = min(len(name) for name in entries)

    longest_names = [name.capitalize() for name in entries if len(name) == max_length]
    shortest_names = [name.capitalize() for name in entries if len(name) == min_length]

    longest_names_str = ', '.join(longest_names)
    shortest_names_str = ', '.join(shortest_names)

    return f'The longest names are {longest_names_str}and the shortest\nnames are {shortest_names_str}.'

file_path = 'names.txt'
print(return_longest_and_shortest_names(file_path))
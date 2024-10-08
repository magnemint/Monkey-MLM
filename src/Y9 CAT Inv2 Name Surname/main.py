from matplotlib import pyplot as grapher

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

def process_name(name):
    name = name.lower()
    if len(name) > 0:
        pairs = [(name[i], name[i + 1]) for i in range(len(name) - 1)]
        start_letter = name[0]
        end_letter = name[-1]
    else:
        pairs = []
        start_letter = ''
        end_letter = ''
    return {
        "pairs": pairs,
        "start_letter": start_letter,
        "end_letter": end_letter
    }

def count_from_names(names):
    pair_counts = {}
    start_counts = {}
    end_counts = {}

    for name in names:
        processed = process_name(name)
        for pair in processed['pairs']:
            if pair in pair_counts:
                pair_counts[pair] += 1
            else:
                pair_counts[pair] = 1
        start_letter = processed['start_letter']
        if start_letter:
            if start_letter in start_counts:
                start_counts[start_letter] += 1
            else:
                start_counts[start_letter] = 1
        end_letter = processed['end_letter']
        if end_letter:
            if end_letter in end_counts:
                end_counts[end_letter] += 1
            else:
                end_counts[end_letter] = 1
    return pair_counts, start_counts, end_counts

def write_pair_freqs_to_file(pair_counts, filename='pair_freqs_raw.txt'):
    sorted_pairs = sorted(pair_counts.items(), key=lambda x: x[1], reverse=True)
    with open(filename, 'w') as f:
        for pair, count in sorted_pairs:
            f.write(f'{pair}: {count}\n')

def write_sorted_pair_to_file(pair_counts, filename='pair_freqs_sorted.txt'):
    sorted_pairs = sorted(pair_counts.items(), key=lambda x: x[0][0])
    with open(filename, 'w') as f:
        for pair, count in sorted_pairs:
            f.write(f'{pair}: {count}\n')

def plot_pair_frequencies(sorted_pairs, quantity):
    pairs, counts = zip(*sorted_pairs[:quantity])
    labels = [f'{p[0]}-{p[1]}' for p in pairs]
    grapher.figure(figsize=(14, 8))
    grapher.bar(labels, counts, color='lightgreen')
    grapher.xlabel('Character Pair')
    grapher.ylabel('Frequency')
    grapher.title(f'First {quantity} Character Pairs by Frequency')
    grapher.xticks(rotation=45, ha='right')
    grapher.grid(axis='y')
    grapher.tight_layout(pad=2.0)
    grapher.savefig(f'first_{quantity}_pairs_histograms.png')
    grapher.show()


def filter_pairs_by_starting_letter(letter, pair_counts):
    return [(pair, counts) for pair, counts in pair_counts.items() if pair[0] == letter]

file_path = 'names.txt'

a, b, c = count_from_names(read_file(file_path))
write_pair_freqs_to_file(a)
write_sorted_pair_to_file(a)
print(read_file(file_path))
print(plot_pair_frequencies(sorted(a.items(), key=lambda x: x[0][0]), 50))
print(filter_pairs_by_starting_letter('f', a))
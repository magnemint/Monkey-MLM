import math

from matplotlib import pyplot as grapher
import random

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

def simulate_rigged_coin_flip():
    odds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    odds_roll = random.choice(odds)

    if odds_roll <= 8:
        flipped_coin = 'tails'
    else:
        flipped_coin = 'heads'

    return flipped_coin


def rigged_coin_flip_unit_test(quantity):
    results = []
    for i in range(quantity):
        results.append(str(simulate_rigged_coin_flip()))

    heads = results.count('heads')
    tails = results.count('tails')

    heads_perc = heads / quantity * 100
    tails_perc = tails / quantity * 100

    return f'Heads: {heads_perc:.2f}%, Tails: {tails_perc:.2f}%'


def simulate_rigged_spinner():
    odds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    odds_roll = random.choice(odds)

    if odds_roll <= 2:
        spun_side = 0
    elif 2 < odds_roll <= 3:
        spun_side = 1
    elif 3 < odds_roll <= 4:
        spun_side = 2
    else:
        spun_side = 3

    return spun_side


def rigged_spinner_unit_test(quantity):
    results = []
    for i in range(quantity):
        results.append(int(simulate_rigged_spinner()))

    zeros = results.count(0)
    ones = results.count(1)
    twos = results.count(2)
    threes = results.count(3)

    zeros_perc = zeros / quantity * 100
    ones_perc = ones / quantity * 100
    twos_perc = twos / quantity * 100
    threes_perc = threes / quantity * 100

    return f'Zeros: {zeros_perc:.2f}%, Ones: {ones_perc:.2f}%, Twos: {twos_perc:.2f}%, Threes: {threes_perc:.2f}%'


def compute_pair_probabilities(pair_counts):
    total_count = sum(pair_counts.values())
    probabilities = {pair: count / total_count * 100 for pair, count in pair_counts.items()}
    return probabilities


def sample_pair(probabilities):
    pairs, probs = zip(*probabilities.items())
    return random.choices(pairs, weights=probs, k=1)[0]


def generate_name(start_letter, second_letter, pair_probabilities):
    start_letter = start_letter.lower()
    if second_letter:
        second_letter = second_letter.lower()

    name = start_letter
    current_letter = start_letter

    if second_letter:
        name += second_letter
        current_letter = second_letter

    max_length = random.randint(3, 9)

    while len(name) < max_length:
        possible_pairs = {pair: prob for pair, prob in pair_probabilities.items() if pair[0] == current_letter}

        if not possible_pairs:
            break

        next_pair = sample_pair(possible_pairs)
        next_letter = next_pair[1]
        name += next_letter
        current_letter = next_letter

    return name


file_path = 'names.txt'

a, b, c = count_from_names(read_file(file_path))
d = compute_pair_probabilities(a)
write_pair_freqs_to_file(a)
write_sorted_pair_to_file(a)
print(read_file(file_path))
plot_pair_frequencies(sorted(a.items(), key=lambda x: x[0][0]), 50)
print(filter_pairs_by_starting_letter('f', a))
print(rigged_coin_flip_unit_test(100))
print(rigged_spinner_unit_test(100))
print(d)
print(generate_name('a', '', d))
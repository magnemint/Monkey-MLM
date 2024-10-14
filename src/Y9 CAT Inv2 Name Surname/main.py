# Imports becuase yes
from matplotlib import pyplot as grapher
import random
import string

def set_style(style, text, end):
    style = style.upper()

    # ANSI Code to make the console text flashy :)
    match style:
        case 'BLACK':
            style = "\033[0;30m"
        case 'RED':
            style = "\033[0;31m"
        case 'GREEN':
            style = "\033[0;32m"
        case 'BROWN':
            style = "\033[0;33m"
        case 'BLUE':
            style = "\033[0;34m"
        case 'PURPLE':
            style = "\033[0;35m"
        case 'CYAN':
            style = "\033[0;36m"
        case 'LIGHT_GRAY':
            style = "\033[0;37m"
        case 'DARK_GRAY':
            style = "\033[1;30m"
        case 'LIGHT_RED':
            style = "\033[1;31m"
        case 'LIGHT_GREEN':
            style = "\033[1;32m"
        case 'YELLOW':
            style = "\033[1;33m"
        case 'LIGHT_BLUE':
            style = "\033[1;34m"
        case 'LIGHT_PURPLE':
            style = "\033[1;35m"
        case 'LIGHT_CYAN':
            style = "\033[1;36m"
        case 'LIGHT_WHITE':
            style = "\033[1;37m"
        case 'BOLD':
            style = "\033[1m"
        case 'FAINT':
            style = "\033[2m"
        case 'ITALIC':
            style = "\033[3m"
        case 'UNDERLINE':
            style = "\033[4m"
        case 'BLINK':
            style = "\033[5m"
        case 'NEGATIVE':
            style = "\033[7m"
        case 'CROSSED':
            style = "\033[9m"
        case 'END':
            style = "\033[0m"
    print(f'{style}{text}\033[0m', end=end)


def read_file(file):
    # Reads file and separates entries to values in a list
    with open(file, 'r') as f:
        entries = f.read().splitlines()
    return entries

def return_longest_and_shortest_names(file):
    # Reads the file
    entries = read_file(file)

    if not entries:
        return 'The file is empty.'

    # Find the shortest and longest names by length using len()
    max_length = max(len(name) for name in entries)
    min_length = min(len(name) for name in entries)

    # Capitalize the all the longest and shortest name(s)
    longest_names = [name.capitalize() for name in entries if len(name) == max_length]
    shortest_names = [name.capitalize() for name in entries if len(name) == min_length]

    # Combines them all to a string
    longest_names_str = ', '.join(longest_names)
    shortest_names_str = ', '.join(shortest_names)

    # Returns a formatted string with all values
    return f'The longest names are {longest_names_str},\nAnd the shortest names are {shortest_names_str}.'


def get_file_stats(file_path):
    # Reads the number of entries in the list
    entries = len(read_file(file_path))

    # Gets the formatted string from the above func
    long_short_str = return_longest_and_shortest_names(file_path)

    # Returns all the statistics as one string
    return f'There are {entries} names in the dataset.\n{long_short_str}'


def process_name(name):
    # Make all the letters in the name to lowercase
    name = name.lower()

    if len(name) > 0:
        # Convert the name into their letter pairs
        pairs = [(name[i], name[i + 1]) for i in range(len(name) - 1)]

        # And get the starting and ending letters
        start_letter = name[0]
        end_letter = name[-1]
    else:
        # The name was blank
        pairs = []
        start_letter = ''
        end_letter = ''

    # Return a dictionary containing the letter pairs and the beginning and end letters
    return {
        "pairs": pairs,
        "start_letter": start_letter,
        "end_letter": end_letter
    }

def count_from_names(names):
    # Initial blank dictionaries
    pair_counts = {}
    start_counts = {}
    end_counts = {}

    for name in names:
        processed = process_name(name)
        for pair in processed['pairs']:
            if pair in pair_counts:
                # If it is already been recorded in the dictionary, increase the count by one
                pair_counts[pair] += 1
            else:
                # Make a new pair in the dictionary and add its counts
                pair_counts[pair] = 1
        start_letter = processed['start_letter']
        if start_letter:
            if start_letter in start_counts:
                # If it is already been recorded in the dictionary, increase the count by one
                start_counts[start_letter] += 1
            else:
                # Make a new pair in the dictionary and add its counts
                start_counts[start_letter] = 1
        end_letter = processed['end_letter']
        if end_letter:
            if end_letter in end_counts:
                # If it is already been recorded in the dictionary, increase the count by one
                end_counts[end_letter] += 1
            else:
                # Make a new pair in the dictionary and add its counts
                end_counts[end_letter] = 1
    return pair_counts, start_counts, end_counts

def write_pair_freqs_to_file(pair_counts, filename='pair_freqs_raw.txt'):
    # Sort the pairs by descending frequency
    sorted_pairs = sorted(pair_counts.items(), key=lambda x: x[1], reverse=True)

    # And write it to a file
    with open(filename, 'w') as f:
        for pair, count in sorted_pairs:
            f.write(f'{pair}: {count}\n')

def write_sorted_pair_to_file(pair_counts, filename='pair_freqs_sorted.txt'):
    # Sort the pairs by alphabetically based on the first letter of each pair
    sorted_pairs = sorted(pair_counts.items(), key=lambda x: x[0][0])

    # And write it to a file
    with open(filename, 'w') as f:
        for pair, count in sorted_pairs:
            f.write(f'{pair}: {count}\n')

def plot_pair_frequencies(sorted_pairs, quantity):
    # Get the pairs and their counts
    pairs, counts = zip(*sorted_pairs[:quantity])
    labels = [f'{p[0]}-{p[1]}' for p in pairs]

    # Open matplotlib and create the graph
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
    # Return all pairs and their counts of the pair's first entry is the letter to sort by
    return [(pair, counts) for pair, counts in pair_counts.items() if pair[0] == letter]

def simulate_rigged_coin_flip():
    # Roll a number between 1 and 10 (inclusive)
    odds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    odds_roll = random.choice(odds)

    # And calculate the odds
    if odds_roll <= 8:
        flipped_coin = 'tails'
    else:
        flipped_coin = 'heads'

    # Return the final verdict
    return flipped_coin


def rigged_coin_flip_unit_test(quantity):
    # Empty list
    results = []

    for i in range(quantity):
        # Run the coin flip for the specified quantity of times and record it in the list
        results.append(str(simulate_rigged_coin_flip()))

    # Count the number of 'heads' and 'tails' in the list
    heads = results.count('heads')
    tails = results.count('tails')

    # Get the percentage
    heads_perc = heads / quantity * 100
    tails_perc = tails / quantity * 100

    # Return a formatted string containing the data
    return f'Heads: {heads_perc:.2f}%, Tails: {tails_perc:.2f}%'


def simulate_rigged_spinner():
    # Roll a number between 1 and 10 (inclusive)
    odds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    odds_roll = random.choice(odds)

    # And calculate the odds
    if odds_roll <= 2:
        spun_side = 0
    elif 2 < odds_roll <= 3:
        spun_side = 1
    elif 3 < odds_roll <= 4:
        spun_side = 2
    else:
        spun_side = 3

    # Return the number spun
    return spun_side


def rigged_spinner_unit_test(quantity):
    # Empty list
    results = []

    for i in range(quantity):
        # Run the coin flip for the specified quantity of times and record it in the list
        results.append(int(simulate_rigged_spinner()))

    # Count the number of 'heads' and 'tails' in the list
    zeros = results.count(0)
    ones = results.count(1)
    twos = results.count(2)
    threes = results.count(3)

    # Get the percentage
    zeros_perc = zeros / quantity * 100
    ones_perc = ones / quantity * 100
    twos_perc = twos / quantity * 100
    threes_perc = threes / quantity * 100

    # Return a formatted string containing the data
    return f'Zeros: {zeros_perc:.2f}%, Ones: {ones_perc:.2f}%, Twos: {twos_perc:.2f}%, Threes: {threes_perc:.2f}%'


def compute_pair_probabilities(pair_counts):
    # Count the total number of frequencies of a starting letter
    total_count = sum(pair_counts.values())

    # Get the probability of the pair's frequency compared to the rest
    probabilities = {pair: count / total_count * 100 for pair, count in pair_counts.items()}

    # Return the probability
    return probabilities


def sample_pair(probabilities, trained=False):
    if trained is True:
        # Get the pair and its probability
        pairs, probs = zip(*probabilities.items())

        # Return a selected pair based on its weight/probability
        return random.choices(pairs, weights=probs, k=1)[0]
    else:
        # Untrained
        return random.choice('abcdefghijklmnopqrstuvwxyz')


def generate_name(start_letter, second_letter, pair_probabilities=None):
    if pair_probabilities is not None:
        # Start with the start letter
        start_letter = start_letter.lower()

        if second_letter:
            # Put the second letter
            second_letter = second_letter.lower()

        # The initial name
        name = start_letter
        current_letter = start_letter

        if second_letter:
            # If there is a second letter justify it
            name += second_letter
            current_letter = second_letter

        # The names min and max values are 3 and 9
        max_length = random.randint(3, 9)

        while len(name) < max_length:
            # Make a dictionary that filters the pair_probabilities dictionary
            possible_pairs = {pair: prob for pair, prob in pair_probabilities.items() if pair[0] == current_letter}

            if not possible_pairs:
                # Something went wrong, or the training is inadequte
                break

            # Generate and add the next few letters
            next_pair = sample_pair(possible_pairs, True)
            next_letter = next_pair[1]
            name += next_letter
            current_letter = next_letter

        # Return the final name
        return name
    else:
        # Not trained generation

        # Start with the start letter
        start_letter = start_letter.lower()

        # Account for the second letter
        if second_letter:
            second_letter = second_letter.lower()

        name = start_letter

        if second_letter:
            # Justify the second letter
            name += second_letter

        # Name should be between 3 and 9 letters
        max_length = random.randint(3, 9)

        while len(name) < max_length:
            # Generate the next few letters and add it
            next_letter = random.choice(string.ascii_lowercase)
            name += next_letter

        # Return the final name
        return name


def evaluate_name_likelihood(name, pair_probabilities):
    name = name.lower()

    # Get the pairs of a name
    pairs = [(name[i], name[i + 1]) for i in range(len(name) - 1)]

    # Collect probabilities for each pair
    pair_probs = {}
    for pair in pairs:
        prob = pair_probabilities.get(pair, 0)
        pair_probs[pair] = prob  # Use 0 if the pair does not exist in probabilities

    # Return their probabilities
    return pair_probs


def compare_name_against_model(name, pair_probabilities):
    # Get the probabilities
    pair_probs = evaluate_name_likelihood(name, pair_probabilities)
    set_style('cyan', f"Pair probabilities for the name '{name}':", '\n')

    for pair, prob in pair_probs.items():
        # Print the probability
        set_style('green', f"Probability of pair {pair}: {prob:.2f}%", '\n')


def prompt(file_location):
    # Print the menu
    prompt_text = '''    (1) Basic statistics (number of names, shortest, longest, etc.)
    (2) Display the first _ lines of the sorted pairs frequency table
    (3) Display pairs starting with a particular character
    (4) Flip the coin and demonstrate correctness
    (5) Spin the numbered wheel and demonstrate correctness
    (6) Generate _ new names starting with letter _
    (7) Generate _ random names
    (8) Demonstrate the result of an untrained character-pair frequency table
    (9) Evaluate a name against the model by printing its pair probabilities'''
    set_style('end', 'Use the menu below to explore the features of \033[1mMonkeyMLM\033[0m:', '\n')
    set_style('cyan', prompt_text, '\n')

    while True:
        # Get the user's input and execute an action
        action = input(
            'Enter \033[1m1\033[0m to \033[1m9\033[0m, \033[1m0\033[0m to quit, or \033[1m-\033[0m to print the options \033[4magain\033[0m: ')
        match(action):
            case '0':
                set_style('cyan', 'Thank you for using MonkeyMLM, have a great day!', '')
                break
            case '-':
                set_style('cyan', prompt_text, '\n')
            case '1':
                stats = input('Would you like to see the statistics of the dataset? (Y/N) ').lower()
                graph = input('Would you like to see a graph of the pair frequencies in the dataset? (Y/N) ').lower()

                if stats == 'y':
                    set_style('blue', get_file_stats(file_location), '\n')

                if graph == 'y':
                    quantity = int(input('How many pairs would you like to see? '))
                    entries = read_file(file_location)
                    pair_counts, _, _ = count_from_names(entries)
                    sorted_pairs = sorted(pair_counts.items(), key=lambda x: x[1], reverse=True)
                    plot_pair_frequencies(sorted_pairs, quantity)
            case '2':
                entries = read_file(file_location)
                pair_counts, _, _ = count_from_names(entries)
                sorted_pairs = sorted(pair_counts.items(), key=lambda x: x[1], reverse=True)
                n = int(input("How many lines would you like to display? "))
                for pair, count in sorted_pairs[:n]:
                    set_style('green', f'{pair}: {count}', '\n')
            case '3':
                letter = input("Enter the starting letter: ").lower()
                entries = read_file(file_location)
                pair_counts, _, _ = count_from_names(entries)
                sorted_filtered_pairs = filter_pairs_by_starting_letter(letter, pair_counts)
                for pair, count in sorted_filtered_pairs:
                    set_style('green', f'{pair}: {count}', '\n')
            case '4':
                quantity = int(input("How many coin flips to test? "))
                set_style('blue', rigged_coin_flip_unit_test(quantity), '\n')
            case '5':
                quantity = int(input("How many spins to test? "))
                set_style('blue', rigged_spinner_unit_test(quantity), '\n')
            case '6':
                quantity = int(input("How many names would you like to generate? "))
                start_letter = input("Enter the starting letter: ").lower()
                second_letter = input("Enter the second letter (leave blank if not necessary): ").lower()
                entries = read_file(file_location)
                pair_counts, _, _ = count_from_names(entries)
                pair_probabilities = compute_pair_probabilities(pair_counts)
                for _ in range(quantity):
                    generated_name = generate_name(start_letter, second_letter, pair_probabilities)
                    set_style('blue', f'Generated name: {generated_name}', '\n')
            case '7':
                quantity = int(input("How many random names would you like to generate? "))
                entries = read_file(file_location)
                pair_counts, _, _ = count_from_names(entries)
                pair_probabilities = compute_pair_probabilities(pair_counts)
                for _ in range(quantity):
                    start_letter = random.choice(string.ascii_lowercase)
                    generated_name = generate_name(start_letter, '', pair_probabilities)
                    set_style('blue', f'Generated name: {generated_name}', '\n')
            case '8':
                quantity = int(input("How many random names would you like to generate? "))
                set_style('yellow', 'The following names used an un-trained frequency table', '\n')
                for _ in range(quantity):
                    start_letter = random.choice(string.ascii_lowercase)
                    generated_name = generate_name(start_letter, '')
                    set_style('blue', f'Generated name: {generated_name}', '\n')
            case '9':
                name = input("Please enter the name to evaluate: ")
                entries = read_file(file_location)
                pair_counts, _, _ = count_from_names(entries)
                pair_probabilities = compute_pair_probabilities(pair_counts)
                print(pair_probabilities)
                compare_name_against_model(name, pair_probabilities)

if __name__ == "__main__":
    # Dataset location
    file = 'names.txt'

    # Activate the program
    prompt(file)
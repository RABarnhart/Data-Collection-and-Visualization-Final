import json
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Read the JSON lines file and parse data
data = []
with open('bookings.jsonl', 'r') as file:
    for line in file:
        record = json.loads(line)
        data.append(record)

# Extract charges for all people
charges = [record["charges"] for record in data]

# Flatten the list of lists
charges_flat = [charge for sublist in charges for charge in sublist]

# Count the occurrences of each word
word_counts = Counter(charges_flat)

# Define a custom color function based on frequency
def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    # Define a linear color map from red to yellow
    colors = [(1, 1, .5), (1, 0, 0)]  # Red, orange, yellow
    cmap = LinearSegmentedColormap.from_list("custom", colors)

    # Calculate the color based on the frequency
    max_freq = max(word_counts.values())
    freq = word_counts[word]
    normalized_freq = freq / max_freq
    rgba = cmap(normalized_freq)

    # Convert RGBA values to integers
    rgba_int = tuple(int(255 * x) for x in rgba[:3])

    return rgba_int

# Create a word cloud with black background and custom color function
wordcloud = WordCloud(width=800, height=400, background_color='black', color_func=color_func).generate_from_frequencies(word_counts)

# Display the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

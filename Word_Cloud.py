import json
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

# Read the JSON lines file and parse data
data = []
with open('bookings.jsonl', 'r') as file:
    for line in file:
        record = json.loads(line)
        data.append(record)

# Extract officers for all people
officers = [record["arresting officer"] for record in data]

# Count the occurrences of each word
word_counts = Counter(officers)

# Define a custom color function based on frequency
def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    # Define a logarithmic mapping from frequency to colors
    colors = [(1, 0, 0), (1, 0, 0), (1, 0.5, 0), (1, 1, 0), (1, 1, 0), (1, 1, 0)]  # Red, orange, yellow
    cmap = LinearSegmentedColormap.from_list("custom", colors)

    # Calculate the logarithmic position along the color map
    max_freq = max(word_counts.values())
    freq = word_counts[word]
    log_freq = 1 - np.log(freq + 1) / np.log(max_freq + 1)  # Logarithmic scaling
    position = log_freq

    # Interpolate colors
    rgba = cmap(position)

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

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
import seaborn as sns

# Download French stopwords
nltk.download('stopwords')
french_stopwords = stopwords.words('french')

# Load the dataset
data = pd.read_excel('cleanData.xlsx')

# Step 1: Clean the text data
def clean_text(text):
    if isinstance(text, str):  # Check if text is a string
        text = text.lower()   # Convert to lowercase
        text = text.replace(',', ' ').replace('.', ' ')  # Remove punctuation
        return ' '.join([word for word in text.split() if word not in french_stopwords])
    return ''

# Apply cleaning to the 'contenu_de_l_info' column
data['cleaned_text'] = data['contenu_de_l_info'].apply(clean_text)

# Step 2: TF-IDF Vectorization
vectorizer = TfidfVectorizer(max_features=100)  # Limit to top 100 words
tfidf_matrix = vectorizer.fit_transform(data['cleaned_text'])
feature_names = vectorizer.get_feature_names_out()

# Get top TF-IDF words for the entire dataset
tfidf_scores = tfidf_matrix.sum(axis=0).A1
word_scores = dict(zip(feature_names, tfidf_scores))

# Step 3: Global Word Cloud
global_wc = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_scores)
plt.figure(figsize=(10, 5))
plt.title('Global Word Cloud')
plt.imshow(global_wc, interpolation='bilinear')
plt.axis('off')
plt.savefig('global_wordcloud.png')
plt.close()

# Step 4: Category-Specific Word Clouds
categories = ['Politique', 'Santé', 'Immigration']

for category in categories:
    # Filter data for the category
    category_data = data[data['thématique'] == category]['cleaned_text']
    if len(category_data) > 0:
        # TF-IDF for the category
        category_tfidf = vectorizer.fit_transform(category_data)
        category_scores = category_tfidf.sum(axis=0).A1
        category_words = dict(zip(vectorizer.get_feature_names_out(), category_scores))
        
        # Generate word cloud
        wc = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(category_words)
        plt.figure(figsize=(10, 5))
        plt.title(f'Word Cloud for {category}')
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(f'wordcloud_{category.lower()}.png')
        plt.close()

# Step 5: Save top TF-IDF words to a text file
with open('top_tfidf_words.txt', 'w', encoding='utf-8') as f:
    f.write('Top TF-IDF Words (Global):\n')
    for word, score in sorted(word_scores.items(), key=lambda x: x[1], reverse=True)[:20]:
        f.write(f'{word}: {score:.4f}\n')

print("Analysis complete! Check the generated word cloud images and 'top_tfidf_words.txt' for results.")
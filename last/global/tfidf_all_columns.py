import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords

# Download French stopwords
nltk.download('stopwords')
french_stopwords = stopwords.words('french')
custom_stopwords = french_stopwords + [
    'https', 'www', 'http', 'texte', 'province', 'québec province',
    '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'
]

# Step 1: Load and display the dataset
print("Loading dataset...")
data = pd.read_excel('cleanData.xlsx')
print("\nFirst 5 rows of the dataset:")
print(data.head())
print("\nDataset info:")
print(data.info())

# Step 2: Select relevant text columns
text_columns = [
    'contenu_de_l_info', 'thématique', 'type_d_infox', 'objectif_possible',
    'public_cible', 'plateforme_de_diffusion', 'format', 'véracité'
]
print(f"\nText columns selected: {text_columns}")

# Step 3: Clean the text data
def clean_text(text):
    if not isinstance(text, str):  # Handle non-string (e.g., NaN)
        return ''
    # Convert to lowercase
    text = text.lower()
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove dates and numbers (e.g., "20/06/2020", "01")
    text = re.sub(r'\b\d{1,2}/\d{1,2}/\d{2,4}\b|\b\d{1,2}\b', '', text)
    # Remove punctuation and special characters
    text = re.sub(r'[^\w\s]', ' ', text)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Step 4: Combine text from selected columns per row
def combine_text(row, text_cols):
    # Clean and combine text from each text column
    return ' '.join(clean_text(row[col]) for col in text_cols if pd.notna(row[col]))

# Fix 'Sané' typo in thématique
data['thématique'] = data['thématique'].replace('Sané', 'Santé')

# Create a new column with combined text
data['combined_text'] = data.apply(lambda row: combine_text(row, text_columns), axis=1)

# Step 5: Prepare documents for TF-IDF
docs = data['combined_text'].tolist()
print(f"\nTotal documents: {len(docs)}")
print(f"Valid documents: {len([d for d in docs if d.strip()])}")
print("\nSample of first 3 documents (after cleaning):")
for i, doc in enumerate(docs[:3]):
    print(f"Doc {i+1}: {doc[:100]}..." if len(doc) > 100 else f"Doc {i+1}: {doc}")

# Step 6: Compute TF-IDF and display top terms
def compute_tfidf(documents):
    # Filter out empty documents
    valid_docs = [doc for doc in documents if doc.strip()]
    if len(valid_docs) < 2:
        print("Not enough valid documents for TF-IDF. Skipping.")
        return None, None
    
    # Initialize TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        max_features=30,  # More terms
        ngram_range=(1, 1),  # Unigrams only to prevent replication
        stop_words=custom_stopwords,  # French and custom stopwords
        token_pattern=r'(?u)\b[\wàâäéèêëîïôöùûüç]+\b',  # French accents
        min_df=5  # Ignore rare terms
    )
    try:
        tfidf_matrix = vectorizer.fit_transform(valid_docs)
        feature_names = vectorizer.get_feature_names_out()
        
        # Calculate average TF-IDF scores per term
        tfidf_scores = tfidf_matrix.mean(axis=0).A1
        term_scores = dict(zip(feature_names, tfidf_scores))
        
        # Sort terms by TF-IDF score
        sorted_terms = sorted(term_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Display top terms
        print("\nTop 30 terms for selected columns (TF-IDF scores):")
        for term, score in sorted_terms:
            print(f"{term}: {score:.4f}")
        
        return term_scores, sorted_terms
    except ValueError as e:
        print(f"Error computing TF-IDF: {e}. Skipping.")
        return None, None

# Compute TF-IDF
term_scores, sorted_terms = compute_tfidf(docs)

# Step 7: Generate and save word cloud
def generate_wordcloud(term_scores, title, filename):
    if not term_scores:
        print(f"No term scores for {title}. Skipping word cloud.")
        return
    
    # Generate word cloud
    wc = WordCloud(
        width=800, 
        height=400, 
        background_color='white', 
        colormap='viridis', 
        min_font_size=10
    ).generate_from_frequencies(term_scores)
    
    # Plot and save word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.title(title, fontsize=16, pad=20)
    plt.axis('off')
    plt.savefig(filename, bbox_inches='tight')
    plt.close()
    print(f"Word cloud saved as {filename}")

# Generate word cloud
generate_wordcloud(term_scores, 'Word Cloud: Selected Columns', 'wordcloud_all_columns.png')

# Step 8: Save TF-IDF results to text file
def save_tfidf_to_text(sorted_terms, file):
    if sorted_terms:
        file.write("TF-IDF Results for Selected Columns:\n")
        for term, score in sorted_terms:
            file.write(f"{term}: {score:.4f}\n")

with open('tfidf_results_all_columns.txt', 'w', encoding='utf-8') as f:
    save_tfidf_to_text(sorted_terms, f)

print("\nAnalysis complete! Check 'tfidf_results_all_columns.txt' for TF-IDF scores and 'wordcloud_all_columns.png' for word cloud.")
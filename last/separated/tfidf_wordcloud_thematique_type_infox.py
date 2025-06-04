import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Step 1: Load and display the dataset
print("Loading dataset...")
data = pd.read_excel('cleanData.xlsx')
print("\nFirst 5 rows of the dataset:")
print(data[['thématique', 'type_d_infox']].head())
print("\nDataset info:")
print(data[['thématique', 'type_d_infox']].info())

# Step 2: Clean the text data
def clean_text(text):
    if not isinstance(text, str):  # Handle non-string (e.g., NaN)
        return ''
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation and special characters
    text = re.sub(r'[^\w\s]', ' ', text)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Apply cleaning to 'thématique' and 'type_d_infox'
data['cleaned_thématique'] = data['thématique'].apply(clean_text)
data['cleaned_type_d_infox'] = data['type_d_infox'].apply(clean_text)

# Step 3: Prepare documents for TF-IDF
# Use each row as a document
docs_thematique = data['cleaned_thématique'].tolist()
docs_type_d_infox = data['cleaned_type_d_infox'].tolist()

# Step 4: Compute TF-IDF and display top terms
def compute_tfidf(documents, column_name):
    # Filter out empty documents
    valid_docs = [doc for doc in documents if doc.strip()]
    if len(valid_docs) < 2:
        print(f"Not enough valid documents for {column_name}. Skipping TF-IDF.")
        return None, None
    
    # Initialize TF-IDF vectorizer with n-grams
    vectorizer = TfidfVectorizer(
        max_features=20,  # Limit to top 20 terms
        ngram_range=(1, 3),  # Capture unigrams, bigrams, trigrams
        token_pattern=r'(?u)\b[\wàâäéèêëîïôöùûüç]+\b'  # Handle French accents
    )
    try:
        tfidf_matrix = vectorizer.fit_transform(valid_docs)
        feature_names = vectorizer.get_feature_names_out()
        
        # Calculate average TF-IDF scores per term
        tfidf_scores = tfidf_matrix.mean(axis=0).A1
        term_scores = dict(zip(feature_names, tfidf_scores))
        
        # Sort terms by TF-IDF score
        sorted_terms = sorted(term_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Display top 20 terms
        print(f"\nTop 20 terms for {column_name} (TF-IDF scores):")
        for term, score in sorted_terms:
            print(f"{term}: {score:.4f}")
        
        return term_scores, sorted_terms
    except ValueError as e:
        print(f"Error computing TF-IDF for {column_name}: {e}. Skipping.")
        return None, None

# Compute TF-IDF for both columns
term_scores_thematique, sorted_terms_thematique = compute_tfidf(docs_thematique, 'thématique')
term_scores_type_d_infox, sorted_terms_type_d_infox = compute_tfidf(docs_type_d_infox, 'type_d_infox')

# Step 5: Generate and save word clouds
def generate_wordcloud(term_scores, title, filename):
    if not term_scores:
        print(f"No term scores for {title}. Skipping word cloud.")
        return
    
    # Generate word cloud
    wc = WordCloud(
        width=800, 
        height=400, 
        background_color='white', 
        colormap='viridis',  # Visually appealing color map
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

# Generate word clouds
generate_wordcloud(term_scores_thematique, 'Word Cloud: Thématique', 'wordcloud_thematique.png')
generate_wordcloud(term_scores_type_d_infox, 'Word Cloud: Type d\'Infox', 'wordcloud_type_d_infox.png')

# Step 6: Save TF-IDF results to text file
def save_tfidf_to_text(sorted_terms, column_name, file):
    if sorted_terms:
        file.write(f"\nTF-IDF Results for {column_name}:\n")
        for term, score in sorted_terms:
            file.write(f"{term}: {score:.4f}\n")

with open('tfidf_results.txt', 'w', encoding='utf-8') as f:
    save_tfidf_to_text(sorted_terms_thematique, 'thématique', f)
    save_tfidf_to_text(sorted_terms_type_d_infox, 'type_d_infox', f)

print(f"\nAnalysis complete! Check 'tfidf_results.txt' for TF-IDF scores and 'wordcloud_thematique.png', 'wordcloud_type_d_infox.png' for word clouds.")
print(f"Document counts: thématique={len([d for d in docs_thematique if d.strip()])}, type_d_infox={len([d for d in docs_type_d_infox if d.strip()])}")
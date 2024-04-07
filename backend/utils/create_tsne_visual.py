import io
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize

from sklearn.manifold import TSNE
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import gensim.downloader as api
import numpy as np

word2vec_model = api.load('word2vec-google-news-300')
default_perplexity = 30

def create_tsne_visualization(txt_file_text):
    tokens = word_tokenize(txt_file_text)
    
    word_vectors = [word2vec_model[word] for word in tokens if word in word2vec_model.key_to_index]
    word_vectors_np = np.array(word_vectors)
        
    perplexity_value = max(1, min(default_perplexity, len(word_vectors_np - 1)))
    if perplexity_value < 0:
        perplexity_value = 1
    tsne = TSNE(n_components=2, perplexity=perplexity_value, random_state=0)
    reduced_vectors = tsne.fit_transform(word_vectors_np)
    
    plt.figure(figsize=(12, 12))
    plt.scatter(reduced_vectors[:, 0], reduced_vectors[:, 1])
    plt.title('t-SNE Visualization')
    plt.xlabel('t-SNE Dimension 1')
    plt.ylabel('t-SNE Dimension 2')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)  # Move the cursor to the beginning of the buffer
    plt.close()  # Close the plot to free memory
    
    return buffer

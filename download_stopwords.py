import nltk
import ssl

# Disable SSL certificate verification
ssl._create_default_https_context = ssl._create_unverified_context

# Set NLTK data path
nltk.data.path.append("C:\\Users\\saurabh.tripathi/nltk_data")

# Download the stopwords resource
nltk.download('stopwords')
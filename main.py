from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import string
from sentence_transformers import SentenceTransformer, util
import pandas as pd


class ImprovementSuggestor():
    """
    The class for making improvement suggestions for provided text

    Methods
    -------
    preprocess_sentences()
        Return preprocessed list of words (tokens)
    get_similar_words(tokenized_text, tokenized_terms, threshold)
        Return list of similar words or sentences (up to 10)
    get_results()
        Return result dataframe with text improvement suggestions
    """

    def __init__(self) -> None:
        """Initialize self. See help(type(self)) for accurate signature."""
        self.model = SentenceTransformer(
            'sentence-transformers/all-MiniLM-L6-v2')

    def preprocess_sentences(self, sentences) -> list:
        '''Return preprocessed list of words (tokens)'''
        lemmatizer = WordNetLemmatizer()
        tokenized_sentences = [word_tokenize(
            sentence.lower()) for sentence in sentences]
        stop_words = set(stopwords.words('english'))
        filtered_sentences = [[lemmatizer.lemmatize(word) for word in sentence if word not in stop_words and (
            word not in string.punctuation) and len(word) > 2] for sentence in tokenized_sentences]

        word_groups = []
        for sentence in filtered_sentences:
            for i in range(len(sentence) - 1):
                word_groups.append(sentence[i] + ' ' + sentence[i+1])
        return word_groups

    def get_similar_words(self, tokenized_text, tokenized_terms, threshold=0.35) -> list:
        '''Return list of similar words or sentences (up to 10)'''
        embeddings = self.model.encode(tokenized_text, convert_to_tensor=True)
        embeddings_terms = self.model.encode(
            tokenized_terms, convert_to_tensor=True)
        cosine_scores = util.cos_sim(embeddings, embeddings_terms)

        pairs = []
        for i in range(len(cosine_scores)-1):
            for j in range(i+1, len(cosine_scores[0])):
                pairs.append({'index': [i, j], 'score': cosine_scores[i][j]})

        pairs = sorted(pairs, key=lambda x: x['score'], reverse=True)
        result = []
        for pair in pairs[0:10]:
            i, j = pair['index']
            if pair['score'] > threshold:
                result.append(
                    (tokenized_text[i], i, tokenized_terms[j], j, round(float(pair['score']), 2)))
        return result

    def get_results(self, sentences: str,
                    terms_path='example_input/Standardised terms.csv') -> pd.DataFrame:
        '''Return result dataframe with text improvement suggestions'''

        terms = pd.read_csv(terms_path)
        terms = self.preprocess_sentences(terms.iloc[:, 0])
        first_tokens = sent_tokenize(sentences)
        second_tokens = self.preprocess_sentences(first_tokens)

        words_result = self.get_similar_words(second_tokens, terms)
        sentence_result = self.get_similar_words(first_tokens, terms)
        words_df = pd.DataFrame(words_result, columns=['word_to_change', 'word_number', 'suggested_word', 'new_word_number', 'similarity']) \
            .sort_values(['word_number', 'similarity'], ascending=[True, False]).reset_index(drop=True)
        sentences_df = pd.DataFrame(sentence_result, columns=['sentence_to_change', 'sentence_number', 'suggested_word', 'new_word_number', 'similarity']) \
            .sort_values(['sentence_number', 'similarity'], ascending=[True, False]).reset_index(drop=True)
        # TODO find position of words in sentences to remove duplicates
        result = pd.concat([words_df.drop(columns=['word_number', 'new_word_number']),
                            sentences_df.drop(columns=['sentence_number', 'new_word_number'])], axis=1)
        result.to_csv('example_output/output.csv')
        return result


# if __name__ == "__main__":
#     sentences = "In today's meeting, we discussed a variety of issues affecting our department. The weather was unusually sunny, a pleasant backdrop to our serious discussions. We came to the consensus that we need to do better in terms of performance. Sally brought doughnuts, which lightened the mood. It's important to make good use of what we have at our disposal. During the coffee break, we talked about the upcoming company picnic. We should aim to be more efficient and look for ways to be more creative in our daily tasks. Growth is essential for our future, but equally important is building strong relationships with our team members. As a reminder, the annual staff survey is due next Friday. Lastly, we agreed that we must take time to look over our plans carefully and consider all angles before moving forward. On a side note, David mentioned that his cat is recovering well from surgery"

#     print(ImprovementSuggestor().get_results(sentences))
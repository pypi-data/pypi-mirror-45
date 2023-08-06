import numpy as np
import pandas as pd
import os
import yaml
import multiprocessing
from gensim.models import Word2Vec
from pyjarowinkler import distance
from azure.storage.file import FileService

class SpellCheck:
    
    def __init__(self, path: str, from_azure: bool = False):
        self.__set_embedding(path, from_azure)
        self.data = None
    
    def __set_embedding(self, path: str, from_azure: bool):
        if from_azure:
            self.__set_embedding_from_azure(path)
            self.__embedding = Word2Vec.load('embedding.model')
        else:
            self.__embedding = Word2Vec.load(path)
            
    def __set_embedding_from_azure(self, config_file_path: str):
        print('Reading config file')
        with open(config_file_path, 'r') as ymlfile:
            config = yaml.load(ymlfile)
        print('Downloading embedding from azure file share')
        file_service = FileService(account_name=config['account_name'], account_key=config['account_key'])
        file_service.get_file_to_path(config['embedding_share'], config['directory'], config['embedding_file'], 'embedding.model')
    
    def set_data(self, data, content_column_name: str = None, file_sep: str = ';', encoding: str = 'utf-8'):
        type_data = type(data)
        
        if type_data == list:
            self.data = pd.Series(data)
        elif type_data == pd.core.frame.Series:
            self.data = data
        elif type_data == pd.core.frame.DataFrame:
            self.data = data[content_column_name] if content_column_name else data.iloc[0]
        elif type_data == str and os.path.isfile(data):
            data = pd.read_csv(data, sep = file_sep, encoding = encoding, usecols = [content_column_name if content_column_name else 0])
            data.columns = ['Content']
            self.data = data['Content']
        else:
            print('Invalid type of text. Text must be of type string, list, series, dataframe or file path')
    
    def __calculate_limits(self, ind: int, sentence_len: int):
        left = ind - self.__window_limit
        right = ind + self.__window_limit
        left_limit = max(0, left)
        right_limit = min(sentence_len, right)
        return left_limit, right_limit
    
    def __find_correct_word(self, ind: int, left_limit: int, right_limit: int, sentence_lst: list):
        left_words = sentence_lst[left_limit:ind][::-1]
        right_words = sentence_lst[ind+1:right_limit]
        similar_words = self.__embedding.predict_output_word(left_words + right_words, topn = 10)
        similar_lst = [distance.get_jaro_distance(similar_word[0], sentence_lst[ind], winkler=False, scaling=0.1) for similar_word in similar_words]
        most_similar_word = similar_words[np.argmax(similar_lst)][0]    
        return most_similar_word, max(similar_lst)
        
    def spell_check_sentence(self, sentence: str):
        sentence_lst = sentence.split()
        mask_wrong = [False if word in self.__embedding.wv.vocab or word.isdigit() else True for word in sentence_lst]
        
        if True in mask_wrong:
            sentence_len = len(sentence_lst)
            for ind, value in enumerate(mask_wrong):
                if value:
                    left_limit, right_limit = self.__calculate_limits(ind,sentence_len)    
                    if False in mask_wrong[left_limit:right_limit]:    
                        most_similar_word, similarity_score = self.__find_correct_word(ind, left_limit, right_limit, sentence_lst)    
                        if similarity_score > self.__threshold:
                            sentence_lst[ind] = most_similar_word
                        
            return ' '.join(sentence_lst)
        return sentence
    
    def spell_check(self, window_limit: int = 5, threshold: float = 0.9, save_result: bool = True, output_file_name: str = 'output_spell_check.csv'):
        print('Starting spell check of {} sentences'.format(self.data.shape[0]))
        self.__threshold = threshold
        self.__window_limit = window_limit
    
        if self.data is not None:
            try:
                print('Started spell checker sentences')
                with multiprocessing.Pool() as pool:
                    spell_checked_sentences = pool.map(self.spell_check_sentence, self.data)
                print('Finished spell checker sentences')
                corrected = [True if spell_checked_sentences[ind] != sentence.strip() else False for ind, sentence in enumerate(self.data)]
            except Exception as e:
                print('Spell checking error: {}'.format(e))
            else:
                result = pd.DataFrame({'Original': self.data, 'Spell Checked': spell_checked_sentences, 'Corrected': corrected})
                if save_result: 
                    print('Saving spell checked file as {}'.format(output_file_name))
                    result.to_csv(output_file_name, sep = ';', encoding = 'utf-8', index=False)
                return result
            finally:
                print('Finished spell check')
            
        else:
            print('The text was not found. Use set_data to pass a string, list, series, dataframe or file path')
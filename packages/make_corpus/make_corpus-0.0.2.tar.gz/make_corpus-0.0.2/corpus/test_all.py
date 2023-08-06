import unittest as ut
import numpy as np
import sys
import corpus

class Test_core_methods(ut.TestCase):
    def setUp(self):
        self.corpus, self.word_to_id, self.id_to_word = corpus.preprocess("You say goodbye and I say hello.")

    def test_corpus(self):
        self.assertEqual(len(self.corpus),8)

    def test_word_to_id(self):
        self.assertEqual(self.word_to_id,{'and': 3, 'i': 4, '.': 6, 'say': 1, 'goodbye': 2, 'you': 0, 'hello': 5})

    def test_id_to_word(self):
        self.assertEqual(self.id_to_word,{0: 'you', 1: 'say', 2: 'goodbye', 3: 'and', 4: 'i', 5: 'hello', 6: '.'})

if __name__=="__main__":
    ut.main()

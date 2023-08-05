from spacy.tokens import Doc, Span
import os
from symspellpy.symspellpy import SymSpell

sym_spell = None
def _load_dictionary(f="frequency_dictionary_en_500_000.txt"):
    global sym_spell
    max_edit_distance_dictionary = 2
    prefix_length = 7
    # create object
    sym_spell = SymSpell(max_edit_distance_dictionary, prefix_length)
    # load dictionary
    dictionary_path = os.path.join(os.path.dirname(__file__), f)
    term_index = 0  # column of the term in the dictionary text file
    count_index = 1  # column of the term frequency in the dictionary text file
    if not sym_spell.load_dictionary(dictionary_path, term_index, count_index, "utf8"):
        print("Dictionary file not found")
        #todo: probably throw exception instead
    return sym_spell

def _get_suggestions(spacy_object, dic="frequency_dictionary_en_500_000.txt"):
    assert isinstance(spacy_object, Doc) or isinstance(spacy_object, Span), "spacy_object must be a spacy Doc or Span object but it is a {}".format(type(spacy_object))
    global sym_spell
    if sym_spell is None:
        _load_dictionary(dic)
    max_edit_distance_lookup = 2
    suggestions = sym_spell.lookup_compound(spacy_object.text,
                                            max_edit_distance_lookup)
    # gets list of suggestion term, edit distance, and term frequency
    return suggestions

def _get_segmentation(spacy_object, dic="frequency_dictionary_en_500_000.txt"):
    assert isinstance(spacy_object, Doc) or isinstance(
        spacy_object, Span), "spacy_object must be a spacy Doc or Span object but it is a {}".format(type(spacy_object))
    global sym_spell
    if sym_spell is None:
        _load_dictionary(dic)
    
    #contains result.corrected_string, result.distance_sum, result.log_prob_sum
    result = sym_spell.word_segmentation(spacy_object.text)
    return result

class SpellingCorrector(object):
    """Spelling correction for spaCy via Symspell.

    Arguments:
        dictionary: An optional dictionary file for symsepll. (Default None).
                                     If None uses the default frequency_dictionary_en_500_000.txt for lookups
                                     You may also specify the smaller frequency_dictionary_en_82_765.txt for possibly faster dictionary loading performance
    """

    def __init__(self, dictionary_path=None):
        if dictionary_path:
            _load_dictionary(dictionary_path)

    def __call__(self, spacy_object):
        assert isinstance(spacy_object, Doc) or isinstance(spacy_object, Span), "spacy_object must be a spacy Doc or Span object but it is a {}".format(type(spacy_object))
        spacy_object.set_extension("suggestions", getter=_get_suggestions)
        spacy_object.set_extension("segmentation", getter=_get_segmentation)
        for sent in spacy_object.sents:
            if sent.get_extension("suggestions") is None:
                sent.set_extension("suggestions", getter=_get_suggestions)
            if sent.get_extension("segmentation") is None:
                sent.set_extension("segmentation", getter=_get_segmentation)
        return spacy_object
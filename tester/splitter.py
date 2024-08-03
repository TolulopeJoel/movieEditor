import nltk
from nltk.tag import pos_tag
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download("punkt")
nltk.download("maxent_ne_chunker")
nltk.download("words")
nltk.download("averaged_perceptron_tagger")


def split_into_phrases(text: str) -> list[str]:
    """
    Split the input text into phrases based 
    on specific part-of-speech (POS) patterns.
    """
    # split into sentences, then further split by commas
    sentences = [
        sentence
        for i in sent_tokenize(text)
        for sentence in i.split(",")
    ]

    all_phrases = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        pos_tags = pos_tag(words)  # POS tagging

        phrases, phrase = [], []
        for index, (word, pos) in enumerate(pos_tags):
            # check if current word is a pronoun and the next word is a verb
            if pos == "PRP" and pos_tags[index + 1][1] == "VBZ":
                # if the phrase has one word, add the pronoun and verb to the phrase
                if len(phrase) == 1:
                    phrase.append(word)
                    phrase.append(pos_tags[index + 1][0])
                # if the phrase has more than one word, complete the current phrase and start a new one
                else:
                    phrases.append(" ".join(phrase))
                    phrase = [word, pos_tags[index + 1][0]]
                # remove the processed verb to avoid reprocessing
                pos_tags.pop(index + 1)
            # if current word is a conjunction, number, determiner, etc., complete the current phrase
            elif pos in {"CC", "CD", "DT", "LS", "VBZ", "MD", "TO"} and phrase:
                phrases.append(" ".join(phrase))
                phrase = [word]
            else:
                phrase.append(word)

        if phrase:
            phrases.append(" ".join(phrase))

        all_phrases.extend(phrases)

    return all_phrases

import sys
from functools import cache

import click
from wiktionaryparser import WiktionaryParser


@cache
def parser():
    return WiktionaryParser()


def translate(word: str) -> str:
    """ connect to wiktionary, get all part of speech, join them into one string, and return here """

    parser = WiktionaryParser()
    def_ = parser.fetch(word.lower())
    ret = ""
    for word_payload in def_:
        definitions = word_payload['definitions']

        translations = {d['partOfSpeech']: "; ".join(d['text'])
                        for d in definitions}
        ret += " ".join(f"{k}: {v}" for k,v in translations.items())

    return ret

@click.group()
def main():
    pass


@main.command()
@click.option("--word")
def single_word(word):
    translation = translate(word)
    print(f'{word} | "{translation}"')

@main.command(help="read words from stdin. Strip everything from first '|'")
def stdin():
    for line in sys.stdin.readlines():
        word = line.strip().split("|")[0]
        translation = translate(word)
        print(f'{word} | "{translation}"')



if __name__ == '__main__':
    main()

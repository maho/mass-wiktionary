import sys
from functools import lru_cache as cache

import click
from wiktionaryparser import WiktionaryParser
from progressbar import progressbar

LINE_DIVIDED="///"

@cache
def parser():
    return WiktionaryParser()


def translate(word: str) -> str:
    """ connect to wiktionary, get all part of speech, join them into one string, and return here """
    global LINE_DIVIDER

    parser = WiktionaryParser()
    def_ = parser.fetch(word.lower())
    ret = ""
    for word_payload in def_:
        definitions = word_payload['definitions']

        translations = {d['partOfSpeech']: LINE_DIVIDER.join(d['text'])
                        for d in definitions}
        ret += LINE_DIVIDER.join(f"{k}: {v}" for k,v in translations.items())

    return ret

@click.group()
@click.option("--line-divider", "-l", default="///")
def main(line_divider):
    global LINE_DIVIDER
    LINE_DIVIDER=line_divider


@main.command()
@click.option("--word")
def single_word(word):
    translation = translate(word)
    print(f'{word} | "{translation}"')

@main.command(help="read words from stdin. Strip everything from first '|'")
@click.option("--output", type=click.File('wb'), required=True)
def stdin(output):
    for line in progressbar(sys.stdin.readlines()):
        word = line.strip().split("|")[0]
        translation = translate(word)
        output.write(f"{word} | {translation}\n".encode("utf-8"))



if __name__ == '__main__':
    main()

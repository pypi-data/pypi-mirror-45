import sys
import random
import argparse
import subprocess
import configparser

from . import config

from .baidu_trans import baidu_translate
from .baidu_trans import all_via_langs


def get_via_langs(src_lang: str, times: int=3):
    via_langs = random.sample(all_via_langs, times)
    
    while src_lang in via_langs:
        via_langs = random.sample(all_via_langs, times)

    return via_langs


def augment(origin_text: str, source_lang: str, via_lang: str):
    trans_result = baidu_translate(origin_text, from_lang=source_lang, to_lang=via_lang)
    return baidu_translate(trans_result, from_lang=via_lang, to_lang=source_lang)


def get_augmented_texts(text: str, src_lang: str, times: int, self_including: bool):
    '''
    params:
        text: str, the text you want to augment
        src_lang: str, the language of the text you provided
        times: int, how many times you want to augment
        self_including: bool, whether the origin text you provided should be included in the output
    '''
    
    aug_texts = []

    if self_including:
        aug_texts.append(text)

    via_langs = get_via_langs(src_lang, times)

    for via_lang in via_langs[:times]:
        aug_texts.append(augment(text, src_lang, via_lang))

    return aug_texts


def check_input_args(args):
    # args.text, args.langauge are required
    are_args_ok = bool(args.text) and bool(args.language) and bool(args.appid) and bool(args.key)

    # args.times is optional
    if not args.times:
        args.times = 3 # augment 3 times by default

    if not are_args_ok:
        print(subprocess.call('txtaug -h', shell=True))

    return are_args_ok


def save_credentials(appid, key):
    config.appid = appid
    config.key = key


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-l', 
        '--language',
        type=str, 
        help='source language code of the input text. reference http://api.fanyi.baidu.com/api/trans/product/apidoc')
    parser.add_argument("-t","--times", type=int, help="times to augment")
    parser.add_argument("-s","--self_including", action='store_true', help="whether to show the input text on output")
    parser.add_argument("-a", "--appid", type=str, help="your baidu api app_id")
    parser.add_argument("-k", "--key", type=str, help="your baidu api key")
    parser.add_argument("-T", "--text", type=str, help="text to be augmented")
    args = parser.parse_args()

    if not check_input_args(args):
        return

    save_credentials(args.appid, args.key)

    aug_texts = get_augmented_texts(
        text=args.text, 
        src_lang=args.language, 
        times=args.times,
        self_including=args.self_including,
    )

    for aug_text in aug_texts:
        print(aug_text)


if __name__ == '__main__':
    main()
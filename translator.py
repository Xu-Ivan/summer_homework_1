from logging import exception
import random
import argparse
import sys
import datetime
from googletrans import Translator


def get_arg():
    parser = argparse.ArgumentParser(
        prog="从文本文档中读取单词并翻译，生成生词本。",
        description="增加可选的编译选项以设置范围、是否随机顺序.\n\
        样例： python3 translator.py -t 0 -l 10 -r 5 -m 2"
    )
    parser.add_argument("-t",
                        dest="top",
                        help="指定从词库中的何处开始生成单词本，默认为开头",
                        type=int,
                        default=0,
    )
    parser.add_argument("-l",
                        dest="length",
                        help="从词库中抽取单词的区间长度，默认为整个单词本的大小。\n\
                            如果输入值大于词库长度，则视为从top开始的整个词库。",
                        type=int,
                        default=sys.maxsize,)
    parser.add_argument("-r",
                        dest="random",
                        help="若在范围内随机抽样，则指定生成的单词本的单词数量。\n\
            若这个量大于区间长度，则无效。",
                        type=int,
                        default=1,
                        )
    parser.add_argument("-m",
                        dest="multi",
                        help="指定一次生成单词本的数量。默认为1.",
                        type=int,
                        default=1,
                        )
    args = parser.parse_args()
    return args.top, args.length, args.random, args.multi


def main(top, length, random, multi):
    try:
        with open("./collection.txt") as f:
            original_lines = []
            while True:
                data1 = f.readline()
                if not data1:
                    break
                if data1 != '\n':
                    original_lines.append(data1.strip())
            time_tag = datetime.datetime.now().strftime("%F %T")
            if top < 0 or top >= len(original_lines):
                top = 0
            if length > len(original_lines) - top:
                length = len(original_lines) - top
            if random != -1:
                if random > length or random <= 0:
                    random = -1
            translator = Translator(service_urls=['translate.google.cn'])

            for i in range(multi):
                if random != -1:
                    zample = random.sample(original_lines[top:top + length],
                                           random)
                else:
                    zample = original_lines[top:top + length]
                with open(f"./output/untranslated_{i+1}_{time_tag}.txt",
                          "w") as g:
                    for idx, each in enumerate(zample):
                        words = each.split(",")
                        g.write(f"第{idx+1}词：")
                        for word in words:
                            g.write(f"{word} ")
                        g.write("\n")
                with open(f"./output/translated_{i+1}_{time_tag}.txt",
                          "w") as g:
                    for idx, each in enumerate(zample):
                        words = each.split(",")
                        g.write(f"第{idx+1}词：")
                        for word in words:
                            g.write(f"{word}: ")
                            try:
                                g.write(f"{translator.translate(word)} ")
                            except:
                                g.write("没翻出来")
                        g.write("\n")
    except Exception as e:
        print(str(e))


if __name__ == "__main__":
    main(*get_arg())
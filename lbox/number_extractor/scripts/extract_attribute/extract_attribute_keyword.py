# Extract sentences containing "$"+Arabic numerals from ClueWeb contents

from os import listdir
from os.path import isfile, join

import re
import argparse
import spacy

nlp = spacy.load('en_core_web_sm')

def extract_dollarsign(input_texts, output_file, attr, pre_pad_num=100, post_pad_num=100):
    """ Extract the sentences containing "$"+Arabic numberals

    @return: the number of instances found
    """

    ins_count = 0
    reg_exp = ".{" + str(pre_pad_num) + "} " + attr + " .{" + str(post_pad_num) + "}"
    print("Search for patterns: " + reg_exp)

    results = re.findall(reg_exp, input_texts, re.S|re.I)
    print("Find {} instances".format(len(results)))

    for res in results:
        doc = nlp(res)
        for sent in doc.sents:
            search_salary = re.search(attr, sent.text, re.I)
            if search_salary:
                search_num = re.search(r"[0-9.,]+[0-9]", sent.text)
                if search_num:
                    ins_count += 1
                    new_sent = sent.text.replace(attr, "ATTR")
                    output_file.write(new_sent + "\n")
                break

    return ins_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-attr", type=str, help="The attribute name whose value is to be extracted.", default="price")
    parser.add_argument("-ifnames", nargs='+', help="The data files to be opened.", default=None)
    parser.add_argument("-dir", type=str, help="The directory to find input files.", default=None)    
    parser.add_argument("-pl", "--padding_left", type=int, help="The number of characters to be extracted to the left of the searched pattern", default=100)
    parser.add_argument("-pr", "--padding_right", type=int, help="The number of characters to be extracted to the right of the searched pattern", default=100)
    args = parser.parse_args()

    ifnames = args.ifnames
    dir = args.dir
    attr = args.attr
    output_fname = str(attr) + "_results.txt"
    pad_left = args.padding_left
    pad_right = args.padding_right
    ins_count = 0
    all_files = []
    with open(output_fname, "w+") as ofile:
        if ifnames:
            all_files += ifnames

        if dir:
            dir_files = [join(dir,f) for f in listdir(dir) if isfile(join(dir, f))]
            all_files += dir_files

        for fname in all_files:
            if "warc.gz.txt" in fname:
                with open(fname, "r", errors='replace') as ifile:
                    doc = ifile.read()
                    ins_count += extract_dollarsign(doc, ofile, attr, pad_left, pad_right)
            
    print("Number of final entries: {}".format(ins_count))

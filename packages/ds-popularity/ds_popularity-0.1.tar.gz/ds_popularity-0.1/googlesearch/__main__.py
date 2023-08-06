import argparse
import csv
from .gsearch import search, result_count, search_term
from multiprocessing.dummy import Pool as ThreadPool
import threading
from functools import partial
import time
import random

lock = threading.Lock()


def search_and_write(file, csv_writer, keyword):
    lock.acquire()
    result = search(keyword)
    csv_writer.writerow([search_term(result), result_count(result)])
    file.flush()
    lock.release()
    time.sleep(random.uniform(3, 6))


def using_csv(infile, outfile, remove_duplicates=False):
    csv_reader = csv.reader(infile)
    csv_writer = csv.writer(outfile)
    seen = []
    for keyword, in csv_reader:
        if remove_duplicates and keyword in seen:
            continue
        else:
            seen.append(keyword)

    pool = ThreadPool(10)
    func = partial(search_and_write, outfile, csv_writer)
    pool.map(func, seen)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('infile',
          help="file of keywords - one item per line",
          type=argparse.FileType('r'))
    parser.add_argument('outfile',
          help="file of keywords,result_count",
          type=argparse.FileType('w'))
    parser.add_argument('--remove-duplicates',
          help="removes duplicates: not recommended, remove before supplying",
          action="store_true")
    args = parser.parse_args()
    using_csv(args.infile, args.outfile, args.remove_duplicates)

import glob
import json
import gzip

from datetime import date
import csv

# this script requires the results of `tmdb.py`
# it shrinks the results to a reasonable size for TLRE demos (~50,000),
# by removing movies that:
#   are "Adult",
#   runtime is less than 1 hr,
#   don't have a poster,
#   don't have any votes

def scrub_chunks():
    """Collate a list of chunk paths into a single dictionary

    Keyword arguments:
    files -- list of paths to g-zipped chunks from `tmdb.py`
    """
    files = glob.glob('chunks/*')
    if len(files) == 0 :
        raise SystemExit("No chunks found in `chunks/`. Did you run `tmdb.py` already?")

    keep = []
    count = 0

    keys = None

    for f in files:
        with gzip.open(f, "r") as zip_ref:
            movies = json.load(zip_ref)
            for m in movies.keys():
                dat = movies[m]
                if dat["vote_count"] >= 5:
                    keep.append(dat)
                    count += 1

                    if keys is None:
                        keys = dat.keys()

    print("Kept %d movies" % count)
    return keys, keep

if __name__ == "__main__":
    keys, keep = scrub_chunks()
    filename = "tmdb_dump_" + str(date.today()) + "_1.csv"

    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(keys)

        for movie in keep:
            writer.writerow(movie.values())

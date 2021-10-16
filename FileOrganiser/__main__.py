import FileOrganiser
import cProfile, pstats
import argparse
from time import sleep

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('watchpath', help='The Directory to watch')
    p.add_argument('-d', '--daemon', help="run as daemon", action='store_true')
    p.add_argument('-r',
                   '--recursive',
                   help="Crawl down directories",
                   action='store_true')
    p.add_argument('--log', help="profile run", action='store_true')
    return p.parse_args()

if __name__ == "__main__":
    args = parse_args()
    fileorg = FileOrganiser(watchpath, recursive=args.recursive)
    if args.log:
        with cProfile.Profile() as pr:
            fileorg.start()
            stats = pstats.Stats(pr)
            stats.sort_stats(pstats.SortKey.TIME)
            stats.dump_stats("fileOrg.profile")
    else:
        fileorg.clean()
    
    if args.daemon and not args.log: 
        fileorg.start()
        try: 
            sleep(100)
        except KeyboardInterrupt:
            fileorg.stop()

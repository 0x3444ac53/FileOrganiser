import FileOrganiser
import cProfile, pstats
import argparse

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
    if args.log:
        with cProfile.Profile() as pr:
            FileOrganiser.clean(args.watchpath, False, recursive=args.recursive)
            stats = pstats.Stats(pr)
            stats.sort_stats(pstats.SortKey.TIME)
            stats.dump_stats("fileOrg.profile")
    else:
        FileOrganiser.clean(args.watchpath, args.daemon, recursive=args.recursive)

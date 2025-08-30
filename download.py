import os
import argparse


def download_kaggle(url, output):
    import kagglehub
    os.environ['KAGGLEHUB_CACHE'] = output
    kagglehub.dataset_download(url)


def main(args):
    if args.use_proxy:
        os.environ['HTTP_PROXY'] = args.proxy
        os.environ['HTTPS_PROXY'] = args.proxy
    if args.where == 'kaggle':
        download_kaggle(args.url, args.output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--where', choices=['kaggle'], help='Where to download the dataset', default='kaggle')
    parser.add_argument('-u', '--url', type=str, help='URL to download')
    parser.add_argument('-o', '--output',default='./', type=str, help='Output directory')
    parser.add_argument('--use_proxy', action='store_true', help='Use proxy')
    parser.add_argument('-p', '--proxy', default='127.0.0.1:7890', help='proxy')
    args = parser.parse_args()

    main(args)

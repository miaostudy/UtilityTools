import os
import argparse
import time
from pathlib import Path
def safe_remove(path, force=False):
    import shutil
    if not path or not os.path.exists(path):
        return False

    items_to_delete = []
    if os.path.isfile(path) or os.path.islink(path):
        items_to_delete.append(path)
    elif os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                items_to_delete.append(os.path.join(root, file))
            for dir in dirs:
                items_to_delete.append(os.path.join(root, dir))
        items_to_delete.append(path)

    print("\nThe following content will be deleted soon:")
    for item in items_to_delete:
        print(f"  - {item}")
    print(f"totally: {len(items_to_delete)}")

    if not force:
        while True:
            confirm = input("\ndelete? (y/n): ").strip().lower()
            if confirm in ['y', 'yes']:
                break
            elif confirm in ['n', 'no']:
                print("canceled")
                return False
            else:
                print("please enter 'y' or 'n'")

    try:
        if os.path.isfile(path) or os.path.islink(path):
            os.unlink(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
        return True
    except Exception as e:
        print(f"Filed to delete {path} : {str(e)}")
        return False

def download_kaggle(url, output):
    import kagglehub, shutil
    os.makedirs(output, exist_ok=True)
    os.environ['KAGGLEHUB_CACHE'] = output

    try:
        username, dataset_name = url.split('/')[-2:]
    except ValueError:
        raise ValueError(f"Invalid url: {url}")


    source_path = None
    max_retry = 5
    retry_delay = 2
    for retry in range(max_retry):
        print(f'Downloading {url}, Attempt #{retry}/{max_retry}')
        try:
            source_path =kagglehub.dataset_download(url)
            break
        except Exception as e:
            print(f'Attempt {retry}: {str(e)}')
            if retry < max_retry - 1:
                print(f'Retry after {retry_delay} seconds.')
                time.sleep(retry_delay)

    if source_path is None:
        raise RuntimeError(f'After attempt {max_retry}, could not download dataset')

    target_path = output
    if not output.endswith(dataset_name):
        target_path = os.path.join(target_path, dataset_name)

    if os.path.exists(target_path):
        if not safe_remove(target_path):
            raise RuntimeError(f"could not delete target path: {target_path}")

    try:
        shutil.move(source_path, target_path)
        print(f"datasets moved to: {target_path}")
    except Exception as e:
        raise RuntimeError(f"failed to move datasets: {str(e)}")

    current_path = Path(source_path).parent
    while current_path and str(current_path) != output:
        if username in str(current_path):
            safe_remove(current_path)
            break
        current_path = current_path.parent

    root_datasets_dir = os.path.join(output, 'datasets')
    if os.path.exists(root_datasets_dir):
        safe_remove(root_datasets_dir)


def main(args):
    if args.use_proxy or args.proxy != '127.0.0.1:7890':
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
    parser.add_argument('-f', '--force', action='store_true', help='force delete files')
    args = parser.parse_args()

    main(args)

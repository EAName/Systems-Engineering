#***********************************************
# File: module1-panamaapi.py
# Purpose: Python script to get the list of files containing information
#          about panama papers
#          1. Identify list of files
#          2. Locate the urls & download gz files
#          3. Extract tsv files from gz files
#          4. Upload files to AWS S3
#************************************************/
import os
import json
import requests
import logging
from zipfile import ZipFile as zp
from datetime import datetime
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter
import awsapi

def generate_urls():
    """Generate panama data dump urls

    :return: list of urls
    """
    urls = []
    url = 'https://offshoreleaks.icij.org/pages/database'

    logging.info('Generating url list from {0}'.format(url))
    request = requests.get(url=url)

    if request.status_code==requests.codes.ok:
        for row in request.text.split('\n'):
            if 'href' in row and ('bahamas' in row or 'offshore' in row or 'panama' in row or 'paradise' in row):
                url = row[row.index('href')+6:row.index('>', row.index('href')+5)-1]

                if url[-4:]=='.zip':
                    urls.append(url)
    else:
        logging.error('Issue with generating url list from {0}'.format(url))

    return urls


def file_download(dir, url):
    """Download individual data dump file given a url into specified directory

    :param dir : directory to store file
    :param url : file url link
    :return: downloaded file name
    """

    url_fn =  url.split('/')[-1]
    abs_fn = dir+url_fn

    logging.info('Downloading ... {0}'.format(url_fn))
    response = requests.get(url)

    try:
        with open(abs_fn, "wb") as f:
            f.write(response.content)
    except:
        logging.error('Issue with file downloading {0}'.format(url_fn))

    return url_fn


def unzip(dir, f):
    """Unzip individual file given a file with absolute path

    :param dir : directory to access zipped file & store extracted file
    :param f: zipped file name
    :return: list of unzipped file name/s
    """

    uz_files = []
    try:
        logging.info('Unzipping ... {0}'.format(dir+f))
        zip=zp(dir+f)
        for zf in zip.namelist():
            uz_files.append(zf)
        zip.extractall(dir)
        #os.remove(dir+f)
    except:
        logging.error('Issue with file unzipping {0}'.format(dir+f))

    return uz_files


def main():
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter, prog='imdbapi.py', description='Searches for imdb dump files & downloads them. after unzipping uploads to AWS. \n ')

    parser.add_argument('-b', '--bucket_name', dest='bucket_name', help='AWS bucket to which files to be uploaded', required=True)
    parser.add_argument('-o', '--object_name', dest='object_name', help='AWS directory to which files to be uploaded')
    parser.add_argument('-d', '--dir', dest='dir', help='Local directory for downloading files & uploading to AWS', required=True)
    parser.add_argument('-l', '--log_lvl', dest='log_lvl', choices=['NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help='Logging level to create logs', default='WARNING')

    args = parser.parse_args()

    bucket_name = args.bucket_name
    object_name = args.object_name
    dir         = args.dir
    log_lvl     = args.log_lvl

    if log_lvl.upper()== 'NOTSET':
        log_level = logging.NOTSET
    elif log_lvl.upper()== 'DEBUG':
        log_level = logging.DEBUG
    elif log_lvl.upper()== 'INFO':
        log_level = logging.INFO
    elif log_lvl.upper()== 'WARNING':
        log_level = logging.WARNING
    elif log_lvl.upper()== 'ERROR':
        log_level = logging.ERROR
    elif log_lvl.upper()== 'CRITICAL':
        log_level = logging.CRITICAL

    # Set up logging
    logging.basicConfig(level=log_level,
                        format='%(levelname)s: %(asctime)s: %(message)s')

    # Add '/' to directory strings if not already present at the end
    if object_name and object_name[-1]!='/':
        object_name += '/'

    if dir[-1]!='/':
        dir += '/'

    # Create dir if not already exists
    if not os.path.exists(dir):
        os.makedirs(dir)

    # Generate imdb urls
    urls = generate_urls()

    files          = []
    unzipped_files = []

    # Download files
    for url in urls:
        files.append(file_download(dir, url))

    # Unzip files
    for f in files:
        unzipped_files.extend(unzip(dir, f))

    # Upload files to AWS S3
    for uf in unzipped_files:
        awsapi.upload_file(bucket_name, dir, uf, object_name)
        #os.remove(uf)


if __name__ == "__main__":

    main()

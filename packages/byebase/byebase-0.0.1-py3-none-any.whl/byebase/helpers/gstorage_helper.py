#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
Create by: @huongnhd
"""
import os
from urlparse import urlparse
from google.cloud import storage

from comm.evar_logging import LOGGER as logger


def gs_path_parse(sgfullpath):
    # START post-processing eventdata. Now assume that we have bucketname, dirinbucket, sgfullpath is a url so we use the urlparse to analyze it
    try:
        urlresult = urlparse(sgfullpath)
        # here we support only gs://abcd so the code bellow is only for gs
        # as an example: if we have outputpath="gs://bachphuresultsamples/Alarm/Linh/aaa"
        # we will have ParseResult(scheme='gs', netloc='bachphuresultsamples', path='/Alarm/Linh/aaa', params='', query='', fragment='')
        bucketname = urlresult.netloc
        # remember to remove the first "/" in the path
        inbucketdir = urlresult.path[1:]
        # END POST-PROCESSING
        retdict = {'bucketname': bucketname, 'bucketdir': inbucketdir}
        return retdict
    except:
        return None


# function for copy from GS to local
# TODO refactor it later into common functions
# TODO we should support more than just google storage (e.g., sftp)
def copy_dir(google_storage_link, dest_temp_dir):
    # TODO: make sure that the desttempdir can hold enough data
    # we assume that the guy who calls this function knows how to prepare the right dir
    gs_bucket_dict = gs_path_parse(google_storage_link)
    bucket_name = gs_bucket_dict['bucketname']
    inbucket_dir = gs_bucket_dict['bucketdir']

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blobs = bucket.list_blobs()
    final_temp_dir = dest_temp_dir + "/" + inbucket_dir
    if not os.path.exists(final_temp_dir):
        os.makedirs(final_temp_dir)
    for blob in blobs:
        # filter only files in resultdir -- analyticsresult dir --
        if (blob.name.find(inbucket_dir) > -1):
            if not (blob.name.endswith("/")):
                logger.debug("DEBUG copy file")
                logger.debug(blob.name)
                # here you can also filter othe files, e.g., do not download _SUCCESS
                blob.download_to_filename(dest_temp_dir + "/" + blob.name)
    return '{}/{}'.format(dest_temp_dir, inbucket_dir)
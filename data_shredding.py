from __future__ import print_function
import os
import sys
from os import listdir
from os.path import isfile, join
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--worker_count', dest="worker_count", required=True)
parser.add_argument('--input_path', dest="input_path", required=True)
parser.add_argument('--output_path', dest="output_path", required=True)
parser.add_argument('--training_data_shred_count', dest="training_data_shred_count", required=True)
parser.add_argument('--trainind_dataset_name', dest="trainind_dataset_name", required=True)
args = parser.parse_args()


# make sure config data is encode it correctly
def encode(value):
    if isinstance(value, type('str')):
        return value
    return value.encode('utf-8')


# the function that load the data from the training blob, partition the data
# and upload it to the container blobs
def partition_and_upload_dataset_to_blob():

    # List the blobs in a training container
    blobs_size = 1
    blobs = []
    for path, _, files in os.walk(args.input_path):
        for name in files:
            blobs.append(os.path.join(name))
            blobs_size += os.path.getsize(os.path.join(args.input_path, path, name))

    print(blobs)
    # the vm / thread count
    worker_count = int(args.worker_count)

    # the file count per vm
    file_count = int(args.training_data_shred_count) // worker_count

    # the file size
    file_size = blobs_size // int(args.training_data_shred_count)

    # local shredded data directory
    shredded_input_path = './tmp'
    if not os.path.exists(shredded_input_path):
        os.makedirs(shredded_input_path)
    
    
    args.output_path = os.path.normpath(args.output_path)

    print('slice dataset to temp directory')
    i = 0
    for itr in range(len(blobs)):
        blob = blobs[itr]
        lines_bytes_size = 0
        alist = []
        with open(os.path.join(args.input_path, blob), 'r') as in_file:
            for line in in_file:
                lines_bytes_size += sys.getsizeof(line)
                alist.append(line)
                if lines_bytes_size >= file_size:
                    with open(os.path.join(
                            shredded_input_path, blob + '_' + str(itr) + '_' + str(i)), 'w') as wr:
                        for item in alist:
                            wr.write(item)
                        lines_bytes_size = 0
                        alist = []
                        i += 1

    # combine shreded files into a one file per node
    alldatafiles = [f for f in listdir(shredded_input_path) if isfile(join(shredded_input_path, f))]
    low_index = 0
    high_index = file_count
    filename = "data.lst"
    for vm_count in range(worker_count):
        blob_name = args.trainind_dataset_name + "-" + "%05d" % (vm_count,)
        if high_index > len(alldatafiles):
            high_index = len(alldatafiles)
        if not os.path.exists(os.path.join(args.output_path, blob_name)):
            os.makedirs(os.path.join(args.output_path, blob_name))
        with open(os.path.join(args.output_path, blob_name, filename), 'w') as outfile:
            for itr in range(low_index, high_index):
                    with open(os.path.join(shredded_input_path, alldatafiles[itr])) as infile:
                        for line in infile:
                            outfile.write(line)
        low_index += file_count
        high_index += file_count

    print('Done')


# begin loading, partitioning and deploying training data
partition_and_upload_dataset_to_blob()
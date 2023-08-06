import os
from azure.storage.blob import BlockBlobService
from azure.storage.blob.baseblobservice import BaseBlobService
import time
from datetime import datetime,timedelta
import threading
from functools import reduce
import json
import subprocess


class AzureStorage(object):
    def __init__(self, AzureStorageCredsFilename=r'Y:\R&D\DB\DB-Files\AzureStorage\AzureBlobStorageCreds.txt'):
        with open(AzureStorageCredsFilename) as BlobStorageCredsFile:
            self.BlobStorageCreds = json.load(BlobStorageCredsFile)
        self.base_blob_service = BaseBlobService(account_name=self.BlobStorageCreds['account_name'], account_key=self.BlobStorageCreds['account_key'])
        self.block_blob_service = BlockBlobService(account_name=self.BlobStorageCreds['account_name'], account_key=self.BlobStorageCreds['account_key'])


    def progress_callback(self, current, total):
        """ monitor blob upload/download process"""
        if total>0:
            transfer_fraction = int(current/total*100)
            if transfer_fraction%10==0:
                print('transfer progress (in MBs): {0:.1f}%'.format(transfer_fraction))


    def create_container(self, container_name):
        containers = self.base_blob_service.list_containers()
        container_names = [c.name for c in containers]
        if container_name not in container_names:
            self.block_blob_service.create_container(container_name)


    # def upload_dataset(self,tfrecords_folder):
    #     for filename in os.listdir(tfrecords_folder):
    #         dataset_folder = tfrecords_folder.split('\\')[-1]
    #         path_src = os.path.join(tfrecords_folder, filename)
    #         path_dest = os.path.join(dataset_folder, filename)
    #         print(path_dest)
    #         upload_rec('tfrecords', path_src=path_src, path_dest=path_dest)



    def download_all_recs(self, folder_base, filename):
        blob_folder_list = [blob.name.split('/')[0] for blob in self.block_blob_service.list_blobs('recs')]
        for rec_name in blob_folder_list:
            t = time.time()
            blobname = rec_name + '/' + filename
            local_path = folder_base + '/' + blobname
            self.download_rec_file(blobname, local_path, rec_name)
            print('elapsed time (last file): ' + str(time.time() - t))

    #  TODO:
    def verify_local_remote_db(self, folder_base):
        blob_folder_list = [blob.name for blob in self.block_blob_service.list_blobs('recs')]
        # blob_folder_list = [blob.name.split('/')[0] for blob in self.block_blob_service.list_blobs('recs')]
        # blob_folder_list = reduce(lambda l, x: l if x in l else l + [x], blob_folder_list, [])
        import glob
        local_paths = glob.glob(folder_base + '/**/video_raw', recursive=True)
        blob_paths = [folder_base + "\\" + rec.replace(r'/', '\\') for rec in blob_folder_list if rec.endswith('video_raw')]
        blob_size_bytes = [blob.properties.content_length for blob in azstore.block_blob_service.list_blobs('recs')]
        files_video_list = [x for x in glob.glob(r'E:\Data II\R&D\DB\DB_Recs_CV' + '/**/video_raw', recursive=True)]
        blob_video_list = [x for x in blob_folder_list['blob_list'] if x.endswith('video_raw')]
        same = [blob == file[file.rfind('rec_'):].replace('\\', '/') for blob, file in
                zip(blob_video_list, files_video_list)]

        return {"blob_list":blob_folder_list,
                "locals_paths": local_paths,
                "blobs_path": blob_paths,
                "blobs_size_bytes": blob_size_bytes,
                "locals_not_blobs": set(local_paths).difference(blob_paths),
                "locals_yes_blobs":set(local_paths).intersection(blob_paths)}


def sas_code():
    azstore = AzureStorage()
    from azure.storage.common import (
        AccessPolicy,
        ResourceTypes,
        AccountPermissions,
    )
    from azure.storage.blob import (
        BlockBlobService,
        ContainerPermissions,
        BlobPermissions,
        PublicAccess,
    )
    token_container = azstore.block_blob_service.generate_account_shared_access_signature(
        ResourceTypes.CONTAINER,
        AccountPermissions.LIST + AccountPermissions.READ,
        datetime.utcnow() + timedelta(days=99),
        datetime.utcnow())
    sas_service_container = BlockBlobService(account_name='rawdatagot', sas_token=token_container)
    a = sas_service_container.list_blobs('recs')
    a_list = [blob.name for blob in a]

    token_blob = azstore.block_blob_service.generate_account_shared_access_signature(
        ResourceTypes.OBJECT,
        AccountPermissions.LIST + AccountPermissions.READ,
        datetime.utcnow() + timedelta(days=99),
        datetime.utcnow())
    sas_service_blob = BlockBlobService(account_name='rawdatagot', sas_token=token_blob)
    sas_service_blob.get_blob_to_path('recs', a_list[0], 'C:\\c.blb')
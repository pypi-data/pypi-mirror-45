# -*- coding: utf-8 -*-

"""
Implement a strategy that, back up database every X seconds, and keep backup
up to Y seconds.

Cloud hosted MongoDB usually has built-in backup strategy.
"""

from __future__ import print_function
import os
import re
import uuid
import boto3
import datetime
import subprocess
from shlex import split as command_to_array

from .config import Config

MONGO_BACKUP_S3_URI = "s3://{}/{}".format(Config.MONGO_BACKUP_S3_BUCKET, Config.MONGO_BACKUP_S3_PREFIX)


def create_gzip_archive_filename(dbname):
    """
    Construct gzip archive file name from template.

    :type dbname: str
    :param dbname:

    :rtype: str
    :return:
    """
    utcnow = datetime.datetime.utcnow()
    guid = str(uuid.uuid4())
    tpl = "{dbname}.{utcnow_formatted}.{guid}.archive.gzip"
    utcnow_formatted = utcnow.strftime("%Y-%m-%d-%H-%M-%S.%f")
    return tpl.format(
        dbname=dbname, utcnow_formatted=utcnow_formatted, guid=guid,
    )


def extract_datetime_from_archive_filename(filename):
    """
    Extract datetime from archive filename.

    :type filename: str
    :param filename:

    :rtype: datetime.datetime
    :return:
    """
    results = re.findall("\d\d\d\d-\d\d-\d\d-\d\d-\d\d-\d\d.\d\d\d\d\d\d", filename)
    if len(results):
        return datetime.datetime.strptime(results[-1], "%Y-%m-%d-%H-%M-%S.%f")
    return None


def backup_to_local(dbname):
    """
    Backup ``dbname`` database to local directory.

    :param dbname:
    :return:
    """
    archive_filename = create_gzip_archive_filename(dbname)
    archive_path = os.path.join(Config.MONGO_BACKUP_DIR, archive_filename)
    mongodump_cmd = "mongodump --archive={archive_path} --db {dbname} --gzip".format(
        archive_path=archive_path, dbname=dbname
    )
    subprocess.call(command_to_array(mongodump_cmd))


def backup_to_local_and_s3(dbname):
    """
    Backup ``dbname`` database to local directory and S3 bucket.

    :param dbname:
    :return:
    """
    archive_filename = create_gzip_archive_filename(dbname)
    archive_path = os.path.join(Config.MONGO_BACKUP_DIR, archive_filename)
    mongodump_cmd = "mongodump --archive={archive_path} --db {dbname} --gzip".format(
        archive_path=archive_path, dbname=dbname
    )
    subprocess.call(command_to_array(mongodump_cmd))

    archive_s3_uri = "{MONGO_BACKUP_S3_URI}/{dbname}/{archive_filename}".format(
        MONGO_BACKUP_S3_URI=MONGO_BACKUP_S3_URI,
        dbname=dbname,
        archive_filename=archive_filename
    )
    s3_cp_cmd = "aws s3 cp {archive_path} {archive_s3_uri} --profile {aws_profile}".format(
        archive_path=archive_path, archive_s3_uri=archive_s3_uri, aws_profile=Config.AWS_PROFILE,
    )
    subprocess.call(command_to_array(s3_cp_cmd))


def remove_expired_backup(dbname, period_days):
    """
    Remove expired backup files.

    :type dbname: str
    :param dbname:

    :type period_days: int
    :param period_days:

    :rtype: None
    :return:
    """
    utcnow = datetime.datetime.utcnow()
    for p in os.listdir(Config.MONGO_BACKUP_DIR):
        if p.startswith(dbname):
            create_at = extract_datetime_from_archive_filename(p)
            if create_at is not None:
                seconds_ago = (utcnow - create_at).total_seconds()
                days_ago = seconds_ago * 1.0 / 24 / 3600
                if days_ago > period_days:
                    msg = "%s created %.1f days ago, remove it" % (p, days_ago)
                    print(msg)
                    os.remove(p)

    ses = boto3.Session(profile_name=Config.AWS_PROFILE)
    s3 = ses.client("s3")
    response = s3.list_objects(
        Bucket=Config.MONGO_BACKUP_S3_BUCKET,
        Prefix="{}/{}".format(Config.MONGO_BACKUP_S3_PREFIX, dbname)
    )
    for obj in response["Contents"]:
        create_at = extract_datetime_from_archive_filename(obj["Key"])
        seconds_ago = (utcnow - create_at).total_seconds()
        days_ago = seconds_ago * 1.0 / 24 / 3600
        if days_ago > period_days:
            msg = "s3://%s/%s created %.1f days ago, remove it" % (Config.MONGO_BACKUP_S3_BUCKET, obj["Key"], days_ago)
            print(msg)
            s3.delete_object(Bucket=Config.MONGO_BACKUP_S3_BUCKET, Key=obj["Key"])

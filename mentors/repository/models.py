from profiles.models import MentorsUser

from django.db import models


# Create your models here.


class Package(models.Model):
    name = models.TextField()
    description = models.TextField()


class PackageUpload(models.Model):
    uploader = models.ForeignKey(MentorsUser)
    package = models.ForeignKey(Package)

    version = models.TextField()
    maintainer = models.TextField()
    section = models.TextField()
    suite = models.TextField()
    qa_status = models.IntegerField()
    component = models.TextField()
    priority = models.TextField()
    closes = models.TextField()
    upload_time = models.DateTimeField()


class BinaryPackage(models.Model):
    upload = models.ForeignKey(PackageUpload)
    arch = models.TextField()


class SourcePackage(models.Model):
    upload = models.ForeignKey(PackageUpload)


class PackageFile(models.Model):
    binary = models.ForeignKey(BinaryPackage)
    source = models.ForeignKey(SourcePackage)
    filename = models.TextField()
    size = models.IntegerField()
    md5sum = models.CharField(max_length=200)

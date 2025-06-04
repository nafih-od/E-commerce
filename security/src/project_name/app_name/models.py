from django.db import models


class PrintClass(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=59)

    def __str__(self):
        return self.name


class PingsLog(models.Model):
    host = models.CharField(max_length=225)

    def __str__(self):
        return self.host


class SslLog(models.Model):
    domain = models.CharField(max_length=200)

    def __str__(self):
        return self.domain


class HttpLog(models.Model):
    domain = models.CharField(max_length=200)

    def __str__(self):
        return self.domain


class SsllabsLog(models.Model):
    domain = models.CharField(max_length=200)

    def __str__(self):
        return self.domain


class CmsLog(models.Model):
    domain = models.CharField(max_length=200)

    def __str__(self):
        return self.domain


class NsLog(models.Model):
    domain = models.CharField(max_length=200)

    def __str__(self):
        return self.domain


class DtLog(models.Model):
    domain = models.CharField(max_length=200)

    def __str__(self):
        return self.domain


class CvLog(models.Model):
    domain = models.CharField(max_length=200)

    def __str__(self):
        return self.tech_name



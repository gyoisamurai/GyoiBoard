from django.db import models
from django.core.validators import FileExtensionValidator


class FileUpload(models.Model):
    # Upload file.
    file = models.FileField(verbose_name='Upload File',
                            upload_to='atd/target/%Y%m%d%H%M%S%f',
                            validators=[FileExtensionValidator(['h5', 'npz'])])
    overview = models.CharField(verbose_name='Overview', max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Target(models.Model):
    # Target.
    name = models.CharField(verbose_name='Target name', max_length=255, blank=False)
    overview = models.CharField(verbose_name='Overview', max_length=255, default='N/A')
    rank = models.CharField(verbose_name='Rank', max_length=10, default='N/A')
    last_scan_date = models.CharField(verbose_name='Last scan date', max_length=255, default='N/A')
    status = models.CharField(verbose_name='Status', max_length=255, default='N/A')
    target_path = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class ScanSettingFGSM(models.Model):
    # Setting of FGSM.
    eps = models.IntegerField(verbose_name='Epsilon', default=0.05)
    eps_step = models.IntegerField(verbose_name='Epsilon Step', default=0.1)
    targeted = models.BooleanField(verbose_name='Targeted', default=False)
    batch_size = models.IntegerField(verbose_name='Batch Size', default=32)


class ScanTarget2(models.Model):
    # Scan Target.
    target_name = models.CharField(verbose_name='Target name', max_length=255)
    target_path = models.CharField(verbose_name='Target Path', max_length=255)
    overview = models.CharField(verbose_name='Overview', max_length=255, default='N/A')
    rank = models.CharField(verbose_name='Rank', max_length=10, default='N/A')
    last_scan_date = models.CharField(verbose_name='Last scan date', max_length=255, default='N/A')
    status = models.CharField(verbose_name='Status', max_length=255, default='N/A')

    def __str__(self):
        return self.name


class ScanResult(models.Model):
    # Scan results.
    result = models.ForeignKey(Target, verbose_name='スキャン結果', related_name='scan_result', on_delete=models.CASCADE)
    scan_result = models.TextField('スキャン結果', blank=True)

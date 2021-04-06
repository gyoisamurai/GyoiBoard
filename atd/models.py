from django.db import models
from django.core.validators import FileExtensionValidator


# Model (Target) Upload.
class FileUpload(models.Model):
    # Upload file.
    file = models.FileField(verbose_name='Upload File',
                            upload_to='atd/target/%Y%m%d%H%M%S%f',
                            validators=[FileExtensionValidator(['h5', 'npz'])])
    overview = models.CharField(verbose_name='Overview', max_length=255, blank=True)
    author = models.CharField(verbose_name='Author', max_length=255, blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)


# Model (Target).
class Target(models.Model):
    # Target.
    name = models.CharField(verbose_name='Model name', max_length=255, blank=False)
    overview = models.CharField(verbose_name='Overview', max_length=255, default='N/A')
    author = models.CharField(verbose_name='Author', max_length=255, blank=False)
    registration_date = models.CharField(verbose_name='Registration', max_length=255, default=False)
    rank = models.CharField(verbose_name='Rank', max_length=10, default='N/A')
    last_scan_date = models.CharField(verbose_name='Last scan date', max_length=255, default='N/A')
    status = models.CharField(verbose_name='Status', max_length=255, default='N/A')
    target_path = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


# Scan Setting of FGSM.
class ScanSettingFGSM(models.Model):
    eps = models.FloatField(verbose_name='Epsilon', default=0.05)
    eps_step = models.FloatField(verbose_name='Epsilon Step', default=0.1)
    targeted = models.BooleanField(verbose_name='Targeted', default=False)
    batch_size = models.IntegerField(verbose_name='Batch Size', default=32)


# Scan Setting of CnW.
class ScanSettingCnW(models.Model):
    confidence = models.FloatField(verbose_name='Confidence', default=0.0)
    batch_size = models.IntegerField(verbose_name='Batch Size', default=1)


# Scan Setting of JSMA.
class ScanSettingJSMA(models.Model):
    theta = models.FloatField(verbose_name='Theta', default=0.1)
    gamma = models.FloatField(verbose_name='Gamma', default=1.0)
    batch_size = models.IntegerField(verbose_name='Batch Size', default=1)


# Scan Result.
class ScanResult(models.Model):
    # Scan results.
    scan_result = models.ForeignKey(Target, on_delete=models.CASCADE)
    scan_id = models.CharField(max_length=36, default='')
    attack_method = models.CharField(max_length=255, default='')


# ATD Scan Result (external).
class ExtScanResult(models.Model):
    class Meta:
        db_table = 'ScanResultTBL'

    scan_id = models.CharField(max_length=36, primary_key=True)
    target_id = models.IntegerField()
    status = models.CharField(max_length=255)
    rank = models.CharField(max_length=255)
    summary = models.CharField(max_length=1000)
    target_path = models.CharField(max_length=255)
    accuracy = models.FloatField()
    x_train_path = models.CharField(max_length=255)
    x_train_num = models.IntegerField()
    y_train_path = models.CharField(max_length=255)
    x_test_path = models.CharField(max_length=255)
    x_test_num = models.IntegerField()
    y_test_path = models.CharField(max_length=255)
    operation_type = models.CharField(max_length=255)
    attack_type = models.CharField(max_length=255)
    attack_method = models.CharField(max_length=255)
    defence_type = models.CharField(max_length=255)
    defence_method = models.CharField(max_length=255)
    exec_start_date = models.CharField(max_length=255)
    exec_end_date = models.CharField(max_length=255)
    report_path = models.CharField(max_length=255)
    report_html = models.CharField(max_length=255)
    report_ipynb = models.CharField(max_length=255)
    lang = models.CharField(max_length=255)


# ATD Scan Result of Evasion (external).
class ExtScanResultEvasion(models.Model):
    class Meta:
        db_table = 'ScanResultEvasionTBL'

    scan_id = models.CharField(max_length=36, primary_key=True)
    target_id = models.IntegerField()
    consequence = models.CharField(max_length=255)
    summary = models.CharField(max_length=1000)
    attack_method = models.CharField(max_length=255)
    accuracy = models.FloatField()


# ATD FGSM's setting (external).
class ExtEvasionFGSM(models.Model):
    class Meta:
        db_table = 'EvasionFGSMTBL'

    target_id = models.IntegerField(primary_key=True)
    scan_id = models.CharField(max_length=36)
    epsilon = models.FloatField()
    epsilon_step = models.FloatField()
    targeted = models.IntegerField()
    batch_size = models.IntegerField()
    countermeasure = models.CharField(max_length=3000)


# ATD CnW's setting (external).
class ExtEvasionCnW(models.Model):
    class Meta:
        db_table = 'EvasionCnWTBL'

    target_id = models.IntegerField(primary_key=True)
    scan_id = models.CharField(max_length=36)
    confidence = models.FloatField()
    batch_size = models.IntegerField()
    countermeasure = models.CharField(max_length=3000)


# ATD JSMA's setting (external).
class ExtEvasionJSMA(models.Model):
    class Meta:
        db_table = 'EvasionJSMATBL'

    target_id = models.IntegerField(primary_key=True)
    scan_id = models.CharField(max_length=36)
    theta = models.FloatField()
    gamma = models.FloatField()
    batch_size = models.IntegerField()
    countermeasure = models.CharField(max_length=3000)

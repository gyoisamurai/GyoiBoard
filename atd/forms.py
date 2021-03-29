import os
from django import forms
from atd.models import FileUpload, Target, ScanResult, ScanSettingFGSM


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ('file', 'overview')


class TargetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rank'].widget.attrs['readonly'] = 'readonly'
        self.fields['last_scan_date'].widget.attrs['readonly'] = 'readonly'
        self.fields['status'].widget.attrs['readonly'] = 'readonly'
        self.fields['target_path'].widget.attrs['readonly'] = 'readonly'

    class Meta:
        model = Target
        fields = ('name', 'overview', 'rank', 'last_scan_date', 'status', 'target_path')


class TargetScanForm(forms.ModelForm):
    class Meta:
        model = ScanResult
        fields = ('result',)


class FGSMSettingForm(forms.ModelForm):
    class Meta:
        model = ScanSettingFGSM
        fields = ('eps', 'eps_step', 'targeted', 'batch_size',)


class ScanResultForm(forms.ModelForm):
    class Meta:
        model = ScanResult
        fields = ('result',)

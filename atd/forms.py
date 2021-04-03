import os
from django import forms
from atd.models import FileUpload, Target, ScanSettingFGSM


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ('file', 'overview', 'author')


class TargetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['registration_date'].widget.attrs['readonly'] = 'readonly'
        self.fields['rank'].widget.attrs['readonly'] = 'readonly'
        self.fields['last_scan_date'].widget.attrs['readonly'] = 'readonly'
        self.fields['status'].widget.attrs['readonly'] = 'readonly'
        self.fields['target_path'].widget.attrs['readonly'] = 'readonly'

    class Meta:
        model = Target
        fields = ('name', 'overview', 'author', 'registration_date', 'rank', 'last_scan_date', 'status', 'target_path')


class FGSMSettingForm(forms.ModelForm):
    class Meta:
        model = ScanSettingFGSM
        fields = ('eps', 'eps_step', 'targeted', 'batch_size',)

import os
from django import forms
from atd.models import FileUpload, Target, ScanSettingFGSM, ScanSettingCnW, ScanSettingJSMA


class UploadFileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = FileUpload
        fields = ('file', 'overview', 'author')


class TargetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

        self.fields['registration_date'].widget.attrs['readonly'] = 'readonly'
        self.fields['rank'].widget.attrs['readonly'] = 'readonly'
        self.fields['last_scan_date'].widget.attrs['readonly'] = 'readonly'
        self.fields['status'].widget.attrs['readonly'] = 'readonly'
        self.fields['target_path'].widget.attrs['readonly'] = 'readonly'

    class Meta:
        model = Target
        fields = ('name', 'overview', 'author', 'registration_date', 'rank', 'last_scan_date', 'status', 'target_path')


# FGSM.
class FGSMSettingForm(forms.ModelForm):
    class Meta:
        model = ScanSettingFGSM
        fields = ('eps', 'eps_step', 'targeted', 'batch_size',)


# CnW.
class CnWSettingForm(forms.ModelForm):
    class Meta:
        model = ScanSettingCnW
        fields = ('confidence', 'batch_size',)


# JSMA.
class JSMASettingForm(forms.ModelForm):
    class Meta:
        model = ScanSettingJSMA
        fields = ('theta', 'gamma', 'batch_size',)

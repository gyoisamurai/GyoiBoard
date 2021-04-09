import os
from django import forms
from atd.models import FileUpload, Target, ScanSettingFGSM, ScanSettingCnW, ScanSettingJSMA


class TargetRegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TargetRegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = FileUpload
        fields = ('file_model', 'file_x_train', 'file_y_train', 'file_x_test', 'file_y_test', 'overview', 'author')


class TargetUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TargetUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = FileUpload
        fields = ('file_model',)


class TargetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

        self.fields['name'].widget.attrs['readonly'] = 'readonly'
        self.fields['x_train'].widget.attrs['readonly'] = 'readonly'
        self.fields['y_train'].widget.attrs['readonly'] = 'readonly'
        self.fields['x_test'].widget.attrs['readonly'] = 'readonly'
        self.fields['y_test'].widget.attrs['readonly'] = 'readonly'
        self.fields['accuracy'].widget.attrs['readonly'] = 'readonly'
        self.fields['registration_date'].widget.attrs['readonly'] = 'readonly'
        self.fields['rank'].widget.attrs['readonly'] = 'readonly'
        self.fields['last_scan_date'].widget.attrs['readonly'] = 'readonly'
        self.fields['status'].widget.attrs['readonly'] = 'readonly'
        self.fields['target_path'].widget.attrs['readonly'] = 'readonly'

    class Meta:
        model = Target
        fields = ('name', 'x_train', 'y_train', 'x_test', 'y_test', 'overview', 'author', 'accuracy',
                  'registration_date', 'rank', 'last_scan_date', 'status', 'target_path')


# FGSM.
class FGSMSettingForm(forms.ModelForm):
    class Meta:
        model = ScanSettingFGSM
        fields = ('epsilon', 'epsilon_step', 'targeted', 'batch_size', 'dataset_num',)


# CnW.
class CnWSettingForm(forms.ModelForm):
    class Meta:
        model = ScanSettingCnW
        fields = ('confidence', 'batch_size', 'dataset_num',)


# JSMA.
class JSMASettingForm(forms.ModelForm):
    class Meta:
        model = ScanSettingJSMA
        fields = ('theta', 'gamma', 'batch_size', 'dataset_num',)

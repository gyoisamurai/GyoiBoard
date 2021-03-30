import os

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django_celery_results.models import TaskResult
from django.conf import settings
from celery.result import AsyncResult

from gyoiboard.tasks import executation
from atd.models import Target, ScanResult, ExtScanResult
from atd.forms import UploadFileForm, TargetForm, FGSMSettingForm
from atd.util import Utilty


# Upload files.
def modelform_upload(request):
    target = Target()
    if request.method == 'POST':
        upload_file = UploadFileForm(request.POST, request.FILES)
        if upload_file.is_valid():
            # Save file.
            saved_file = upload_file.save()

            # Update Target model.
            target.name = request.FILES['file']
            target.overview = request.POST['overview']
            target.target_path = saved_file.file.url
            target.save()
            return redirect('atd:target_list')
    else:
        form = UploadFileForm()
    return render(request, 'atd/modelform_upload.html', {'form': form})


# Target list.
def target_list(request):
    targets = Target.objects.all().order_by('id')
    return render(request, 'atd/target_list.html', {'targets': targets})


# Edit Target's information.
def target_edit(request, target_id=None):
    if target_id:
        target = get_object_or_404(Target, pk=target_id)
    else:
        target = Target()

    if request.method == 'POST':
        form = TargetForm(request.POST, instance=target)
        if form.is_valid():
            target = form.save(commit=False)
            target.save()
            return redirect('atd:target_list')
    else:
        form = TargetForm(instance=target)

    return render(request, 'atd/target_edit.html', dict(form=form, target_id=target_id))


# Select scan.
def scan_target(request, target_id):
    if target_id:
        target = get_object_or_404(Target, pk=target_id)
    else:
        return redirect('atd:target_list')

    return render(request, 'atd/scan_select.html', dict(target_id=target_id))


# Scan Setting.
def scan_setting(request, target_id):
    utility = Utilty()

    if target_id:
        # Select Attack Method's form.
        attack_method = ''
        if request.POST['tags'] == 'evasion_fgsm':
            attack_method = utility.transform_attack_method_name(request.POST['tags'])
            setting_form = FGSMSettingForm()
        else:
            # TODO: 他の攻撃手法のフォームを用意すること。
            attack_method = 'Fast Gradient Signed Method'
            setting_form = FGSMSettingForm()
    else:
        return redirect('atd:target_list')

    return render(request, 'atd/scan_setting.html', dict(form=setting_form,
                                                         target_id=target_id,
                                                         attack_id=request.POST['tags'],
                                                         attack_method=attack_method))


# Build ATD's command.
def build_atd_command(scan_id, params, target):
    model_path = '/home/itakaesu/PycharmProjects/GyoiBoard' + target.target_path
    common = '--scan_id {} --op_type attack --model_name {}'.format(scan_id, model_path)
    common_test_data = '--test_data_name X_test.npz --test_label_name y_test.npz --use_x_test_num 100'
    if params['attack_id'] == 'evasion_fgsm':
        specify_option = '--attack_type evasion --attack_evasion fgsm --fgsm_epsilon {}'.format(params['eps'])
    else:
        # TODO: 他のオプションを組み立てる。
        specify_option = '--attack_type evasion --attack_evasion fgsm --fgsm_epsilon {}'.format(params['eps'])
    return common + ' ' + common_test_data + ' ' + specify_option


# Scan Execution.
def scan_exec(request, target_id):
    utility = Utilty()

    if target_id:
        target = get_object_or_404(Target, pk=target_id)
    else:
        return redirect('atd:target_list')

    # Execution.
    scan_id = utility.get_random_token(36)
    command_option = build_atd_command(scan_id, request.POST, target)
    command = 'python3 {}atd.py {}'.format(settings.ATD_DIR, command_option)
    task = executation.delay('{}'.format(command))
    print(scan_id, command)

    # Update to ScanResult.
    scan_result = ScanResult()
    scan_result.scan_result = target
    scan_result.scan_id = scan_id
    scan_result.attack_method = utility.transform_attack_method_name(request.POST['attack_id'])
    scan_result.save()

    return redirect('atd:target_list')


# Scan result's list.
def scan_result_list(request, target_id):
    if target_id:
        target = get_object_or_404(Target, pk=target_id)
        scan_results = ScanResult.objects.filter(scan_result__exact=target_id)
    else:
        return redirect('atd:target_list')

    scan_details = []
    for scan_result in scan_results:
        scan_detail = ExtScanResult.objects.db_manager('atd').filter(scan_id__exact=scan_result.scan_id)
        if len(scan_detail) != 0:
            scan_details.append(scan_detail[0])

    return render(request, 'atd/scan_result_list.html', dict(target=target,
                                                             scan_details=scan_details))


# Execute fix.
def target_fix(request, target_id):
    return


# Delete Target's information.
def target_del(request, target_id):
    target = get_object_or_404(Target, pk=target_id)
    target.delete()
    return redirect('atd:target_list')

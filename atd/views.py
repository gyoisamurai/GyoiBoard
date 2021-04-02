import os
import shutil

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django_celery_results.models import TaskResult
from django.conf import settings
from celery.result import AsyncResult

from gyoiboard.tasks import executation
from atd.models import Target, ScanResult, ExtScanResult, ExtScanResultEvasion, ExtEvasionFGSM
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
def scan_result(request, target_id):
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


# Show scan report (html).
def show_report(request):
    params = request.POST
    if len(params) == 0:
        return redirect('atd:target_list')

    scan_result = ExtScanResult.objects.db_manager('atd').filter(scan_id__exact=params['scan_id'])
    if len(scan_result) == 0:
        return redirect('atd:target_list')
    else:
        scan_result = scan_result[0]

    report_dir = os.path.join(settings.BASE_DIR, 'atd', 'reports', scan_result.report_path.split(os.sep)[-1])
    if os.path.exists(report_dir) is False:
        shutil.copytree(scan_result.report_path, report_dir)

    target = {'dataset_img': {}}
    data_poisoning = {}
    model_poisoning = {}
    evasion = {}
    exfiltration = {}
    target['rank'] = scan_result.rank
    target['summary'] = scan_result.summary
    target['model_path'] = scan_result.target_path
    target['dataset_path'] = scan_result.x_test_path
    target['dataset_num'] = scan_result.x_test_num
    target['accuracy'] = scan_result.accuracy
    target['dataset_img']['img1'] = os.path.join(report_dir, 'img', 'adv_benign_1.jpg')
    if params['attack_type'] == 'evasion':
        evasion['exist'] = True
        evasion_result = ExtScanResultEvasion.objects.db_manager('atd').filter(scan_id__exact=params['scan_id'])
        if len(evasion_result) == 0:
            return redirect('atd:target_list')
        evasion_result = evasion_result[0]
        evasion['consequence'] = evasion_result.consequence
        evasion['summary'] = evasion_result.summary

        if params['attack_method'] == 'fgsm':
            evasion['fgsm'] = {'exist': True}
            fgsm_result = ExtEvasionFGSM.objects.db_manager('atd').filter(scan_id__exact=params['scan_id'])
            if len(fgsm_result) == 0:
                return redirect('atd:target_list')
            fgsm_result = fgsm_result[0]
            evasion['fgsm']['date'] = scan_result.exec_end_date
            evasion['fgsm']['consequence'] = evasion_result.consequence
            evasion['fgsm']['ipynb'] = os.path.join(report_dir, 'evasion_fgsm.ipynb')
            evasion['fgsm']['countermeasure'] = 'Adversarial Training, Feature Squeezing'
            evasion['fgsm']['img1'] = os.path.join(report_dir, 'img', 'adv_fgsm_1.jpg')
            evasion['fgsm']['aes_path'] = os.path.join(report_dir, 'adv_fgsm.npz')
        else:
            # TODO: 他の攻撃手法（CnW, JSMA）を追加すること。
            print()
    else:
        # TODO: 他の攻撃手法を追加すること。
        print()
    return render(request, 'atd/scan_report.html', dict(target=target, evasion=evasion))


# Show scan report (ipynb).
def download_report(request):
    print()

    return render(request, 'atd/target_list.html')


# Execute fix.
def target_fix(request, target_id):
    return


# Delete Target's information.
def target_del(request, target_id):
    target = get_object_or_404(Target, pk=target_id)
    target.delete()
    return redirect('atd:target_list')

import os
import shutil
from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse
from django.conf import settings

from gyoiboard.tasks import executation
from atd.models import Target, ScanResult, ExtScanResult, \
    ExtScanResultEvasion, ScanSettingFGSM, ScanSettingCnW, ScanSettingJSMA, ExtEvasionFGSM, ExtEvasionCnW, ExtEvasionJSMA
from atd.forms import UploadFileForm, TargetForm, FGSMSettingForm, CnWSettingForm, JSMASettingForm
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
            target.author = request.POST['author']
            target.registration_date = saved_file.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')
            target.target_path = saved_file.file.url
            target.save()
            return redirect('atd:target_list')
    else:
        form = UploadFileForm()
    return render(request, 'atd/modelform_upload.html', {'form': form})


# Top Page.
def top_page(request):
    targets = Target.objects.all().order_by('id')
    return render(request, 'atd/index.html', {'targets': targets})


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


# Get specify record using target id, attack method.
def select_specify_record(target_id, attack_method):
    scan_result = ScanResult.objects.filter(scan_result__exact=target_id,
                                            attack_method__exact=attack_method).order_by('id').reverse().first()
    if scan_result is None:
        return None
    else:
        return ExtScanResult.objects.db_manager('atd').filter(scan_id__exact=scan_result.scan_id)


# Get all scan results.
def get_scan_results(target_id):
    if target_id:
        target = get_object_or_404(Target, pk=target_id)
    else:
        return redirect('atd:target_list')

    data_poisoning = {'data_poisoning_fc': {}, 'data_poisoning_cp': {}, 'data_poisoning_bp': {}}
    model_poisoning = {'model_poisoning_ni': {}, 'model_poisoning_mli': {}}
    evasion = {'evasion_fgsm': {}, 'evasion_cnw': {}, 'evasion_jsma': {}}
    exfiltration = {'exfiltration_mi': {}, 'exfiltration_lomi': {}, 'exfiltration_minv': {}}
    for attack_type in ['data_poisoning', 'model_poisoning', 'evasion', 'exfiltration']:
        # Data Poisoning.
        if attack_type == 'data_poisoning':
            for attack_method in ['data_poisoning_fc', 'data_poisoning_cp', 'data_poisoning_bp']:
                scan_detail = select_specify_record(target_id, attack_method)
                if scan_detail is None:
                    continue
                else:
                    data_poisoning[attack_method] = scan_detail[0]
        # Model Poisoning.
        elif attack_type == 'model_poisoning':
            for attack_method in ['model_poisoning_ni', 'model_poisoning_mli']:
                scan_detail = select_specify_record(target_id, attack_method)
                if scan_detail is None:
                    continue
                else:
                    model_poisoning[attack_method] = scan_detail[0]
        # Evasion.
        elif attack_type == 'evasion':
            for attack_method in ['evasion_fgsm', 'evasion_cnw', 'evasion_jsma']:
                scan_detail = select_specify_record(target_id, attack_method)
                if scan_detail is None or len(scan_detail) == 0:
                    continue
                result = ExtScanResultEvasion.objects.db_manager('atd').filter(scan_id__exact=scan_detail[0].scan_id)
                if len(result) == 0:
                    continue
                else:
                    result = result[0]
                    scan_detail[0].accuracy = result.accuracy
                    evasion[attack_method] = scan_detail[0]
        # Exfiltration.
        elif attack_type == 'exfiltration':
            for attack_method in ['exfiltration_mi', 'exfiltration_lomi', 'exfiltration_minv']:
                scan_detail = select_specify_record(target_id, attack_method)
                if scan_detail is None:
                    continue
                else:
                    exfiltration[attack_method] = scan_detail[0]
        else:
            return redirect('atd:target_list')

    return target, data_poisoning, model_poisoning, evasion, exfiltration


# Scanning dashboard.
def scan_detail(request, target_id):
    # Get all scan's results.
    target, data_poisoning, model_poisoning, evasion, exfiltration = get_scan_results(target_id)
    return render(request, 'atd/scan_detail.html', dict(target=target,
                                                        data_poisoning=data_poisoning,
                                                        model_poisoning=model_poisoning,
                                                        evasion=evasion,
                                                        exfiltration=exfiltration))


# Scan Setting.
def scan_setting(request, target_id):
    utility = Utilty()

    if target_id:
        # Select Attack Method's form.
        attack_method = ''
        if request.POST['method'] == 'evasion_fgsm':
            attack_method = utility.transform_attack_method_name(request.POST['method'])
            setting_form = FGSMSettingForm()
        elif request.POST['method'] == 'evasion_cnw':
            attack_method = utility.transform_attack_method_name(request.POST['method'])
            setting_form = CnWSettingForm()
        elif request.POST['method'] == 'evasion_jsma':
            attack_method = utility.transform_attack_method_name(request.POST['method'])
            setting_form = JSMASettingForm()
        else:
            # TODO: 他の攻撃手法のフォームを用意すること。
            attack_method = 'Fast Gradient Signed Method'
            setting_form = FGSMSettingForm()
    else:
        return redirect('atd:target_list')

    return render(request, 'atd/scan_setting.html', dict(form=setting_form,
                                                         target_id=target_id,
                                                         attack_id=request.POST['method'],
                                                         attack_method=attack_method))


# Update scan setting.
def update_setting(request, target_id):
    params = request.POST
    # Insert/Update EvasionFGSMTBL
    if params['attack_id'] == 'evasion_fgsm':
        targeted = 0
        if 'targeted' in params.keys():
            targeted = 1
        fgsm_setting = ExtEvasionFGSM(target_id=target_id,
                                      epsilon=params['eps'],
                                      epsilon_step=params['eps_step'],
                                      targeted=targeted,
                                      batch_size=params['batch_size'])
        fgsm_setting.save()
    # Insert/Update EvasionCnWTBL
    elif params['attack_id'] == 'evasion_cnw':
        cnw_setting = ExtEvasionCnW(target_id=target_id,
                                    confidence=params['confidence'],
                                    batch_size=params['batch_size'])
        cnw_setting.save()
    # Insert/Update EvasionJSMATBL
    elif params['attack_id'] == 'evasion_jsma':
        jsma_setting = ExtEvasionJSMA(target_id=target_id,
                                      theta=params['theta'],
                                      gamma=params['gamma'],
                                      batch_size=params['batch_size'])
        jsma_setting.save()
    else:
        # TODO: 他の攻撃手法の設定更新を追加すること。
        return redirect('atd:target_list')

    # Get all scan's results.
    target, data_poisoning, model_poisoning, evasion, exfiltration = get_scan_results(target_id)
    return render(request, 'atd/scan_detail.html', dict(target=target,
                                                        data_poisoning=data_poisoning,
                                                        model_poisoning=model_poisoning,
                                                        evasion=evasion,
                                                        exfiltration=exfiltration))


# Build ATD's command.
def build_atd_command(scan_id, params, target):
    model_path = '/home/itakaesu/PycharmProjects/GyoiBoard' + target.target_path
    common = '--target_id {} --scan_id {} --op_type attack --model_name {}'.format(target.id, scan_id, model_path)
    common_test_data = '--test_data_name X_test.npz --test_label_name y_test.npz --use_x_test_num 100'

    # Build attack's parameters.
    # FGSM.
    if params['method'] == 'evasion_fgsm':
        specify_option = '--attack_type evasion --attack_evasion fgsm'
        fgsm_setting = ExtEvasionFGSM.objects.filter(target_id__exact=target.id)
        if len(fgsm_setting) != 0:
            # Setting of DB.
            specify_option += ' --fgsm_epsilon {}'.format(fgsm_setting[0].epsilon)
            specify_option += ' --fgsm_eps_step {}'.format(fgsm_setting[0].epsilon_step)
            if fgsm_setting[0].targeted == 1:
                specify_option += ' --fgsm_targeted'
            specify_option += ' --fgsm_batch_size {}'.format(fgsm_setting[0].batch_size)
        else:
            # Default setting.
            fgsm_setting = ScanSettingFGSM()
            specify_option += ' --fgsm_epsilon {}'.format(fgsm_setting.eps)
            specify_option += ' --fgsm_eps_step {}'.format(fgsm_setting.eps_step)
            specify_option += ' --fgsm_batch_size {}'.format(fgsm_setting.batch_size)
    # CnW.
    elif params['method'] == 'evasion_cnw':
        specify_option = '--attack_type evasion --attack_evasion cnw'
        cnw_setting = ExtEvasionCnW.objects.filter(target_id__exact=target.id)
        if len(cnw_setting) != 0:
            # Setting of DB.
            specify_option += ' --cnw_confidence {}'.format(cnw_setting[0].confidence)
            specify_option += ' --cnw_batch_size {}'.format(cnw_setting[0].batch_size)
        else:
            # Default setting.
            cnw_setting = ScanSettingCnW()
            specify_option += ' --cnw_confidence {}'.format(cnw_setting.confidence)
            specify_option += ' --cnw_batch_size {}'.format(cnw_setting.batch_size)
    # JSMA.
    elif params['method'] == 'evasion_jsma':
        specify_option = '--attack_type evasion --attack_evasion jsma'
        jsma_setting = ExtEvasionJSMA.objects.filter(target_id__exact=target.id)
        if len(jsma_setting) != 0:
            # Setting of DB.
            specify_option += ' --jsma_theta {}'.format(jsma_setting[0].theta)
            specify_option += ' --jsma_gamma {}'.format(jsma_setting[0].gamma)
            specify_option += ' --jsma_batch_size {}'.format(jsma_setting[0].batch_size)
        else:
            # Default setting.
            jsma_setting = ScanSettingJSMA()
            specify_option += ' --jsma_theta {}'.format(jsma_setting.theta)
            specify_option += ' --jsma_gamma {}'.format(jsma_setting.gamma)
            specify_option += ' --jsma_batch_size {}'.format(jsma_setting.batch_size)
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

    # Update to ScanResult.
    scan_result = ScanResult()
    scan_result.scan_result = target
    scan_result.scan_id = scan_id
    scan_result.attack_method = request.POST['method']
    scan_result.save()

    # Get all scan's results.
    target, data_poisoning, model_poisoning, evasion, exfiltration = get_scan_results(target_id)
    return render(request, 'atd/scan_detail.html', dict(target=target,
                                                        data_poisoning=data_poisoning,
                                                        model_poisoning=model_poisoning,
                                                        evasion=evasion,
                                                        exfiltration=exfiltration))


# Show scan report (html).
def report(request):
    params = request.POST
    if len(params) == 0:
        return redirect('atd:target_list')

    scan_result = ExtScanResult.objects.db_manager('atd').filter(scan_id__exact=params['scan_id'])
    if len(scan_result) == 0:
        return redirect('atd:target_list')
    else:
        scan_result = scan_result[0]

    # Click "show" button.
    if params['operation'] == 'view':
        # Copy report's "img" dir to static dir on gyoiboard.
        copy_report_to = os.path.join(settings.BASE_DIR, 'atd', 'static', 'atd', 'img', 'report')
        report_dir = os.path.join(copy_report_to, scan_result.report_path.split(os.sep)[-1], 'img')
        if os.path.exists(report_dir) is False:
            shutil.copytree(os.path.join(scan_result.report_path, 'img'), report_dir)

        # Build report's items.
        target = {}
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
        target['dataset_img'] = scan_result.report_path.split(os.sep)[-1]
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
                evasion['fgsm']['accuracy'] = evasion_result.accuracy
                evasion['fgsm']['ipynb'] = os.path.join(report_dir, 'evasion_fgsm.ipynb')
                evasion['fgsm']['countermeasure'] = 'Adversarial Training, Feature Squeezing'
                evasion['fgsm']['aes_path'] = os.path.join(report_dir, 'adv_fgsm.npz')
            elif params['attack_method'] == 'jsma':
                evasion['jsma'] = {'exist': True}
                jsma_result = ExtEvasionJSMA.objects.db_manager('atd').filter(scan_id__exact=params['scan_id'])
                if len(jsma_result) == 0:
                    return redirect('atd:target_list')
                jsma_result = jsma_result[0]
                evasion['jsma']['date'] = scan_result.exec_end_date
                evasion['jsma']['consequence'] = evasion_result.consequence
                evasion['jsma']['accuracy'] = evasion_result.accuracy
                evasion['jsma']['ipynb'] = os.path.join(report_dir, 'evasion_jsma.ipynb')
                evasion['jsma']['countermeasure'] = 'Adversarial Training, Feature Squeezing'
                evasion['jsma']['aes_path'] = os.path.join(report_dir, 'adv_jsma.npz')
            elif params['attack_method'] == 'cnw':
                evasion['cnw'] = {'exist': True}
                cnw_result = ExtEvasionCnW.objects.db_manager('atd').filter(scan_id__exact=params['scan_id'])
                if len(cnw_result) == 0:
                    return redirect('atd:target_list')
                cnw_result = cnw_result[0]
                evasion['cnw']['date'] = scan_result.exec_end_date
                evasion['cnw']['consequence'] = evasion_result.consequence
                evasion['cnw']['accuracy'] = evasion_result.accuracy
                evasion['cnw']['ipynb'] = os.path.join(report_dir, 'evasion_cnw.ipynb')
                evasion['cnw']['countermeasure'] = 'Adversarial Training, Feature Squeezing'
                evasion['cnw']['aes_path'] = os.path.join(report_dir, 'adv_cnw.npz')
            else:
                # TODO: 他の攻撃手法（CnW, JSMA）を追加すること。
                print()
        else:
            # TODO: 他の攻撃手法を追加すること。
            print()
        return render(request, 'atd/scan_report.html', dict(target=target, evasion=evasion))
    # Click "download" button.
    elif params['operation'] == 'download':
        # Copy report's dir to media dir on gyoiboard.
        extension = 'zip'
        copy_media_to = os.path.join(settings.BASE_DIR, 'media', 'atd', 'report')
        file_path = os.path.join(copy_media_to, scan_result.report_path.split(os.sep)[-1])
        if os.path.exists(file_path + '.' + extension) is False:
            shutil.make_archive(file_path, extension, root_dir=scan_result.report_path)
        filename = (file_path + '.' + extension).split(os.sep)[-1]
        return FileResponse(open(file_path + '.' + extension, 'rb'), as_attachment=True, filename=filename)
    else:
        return redirect('atd:target_list')


# Execute fix.
def target_fix(request, target_id):
    return


# Delete Target's information.
def target_del(request, target_id):
    target = get_object_or_404(Target, pk=target_id)
    target.delete()
    return redirect('atd:target_list')

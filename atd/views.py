import os
import shutil

from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse
from django.conf import settings
from django.contrib import messages

from gyoiboard.tasks import executation
from atd.models import Target, ScanResult, ExtScanResult, \
    ExtScanResultEvasion, ScanSettingFGSM, ScanSettingCnW, ScanSettingJSMA, ExtEvasionFGSM, ExtEvasionCnW, ExtEvasionJSMA
from atd.forms import TargetRegistrationForm, TargetUpdateForm, TargetForm, \
    FGSMSettingForm, CnWSettingForm, JSMASettingForm
from atd.util import Utilty


# Upload files.
def modelform_upload(request):
    target = Target()
    if request.method == 'POST':
        upload_file = TargetRegistrationForm(request.POST, request.FILES)
        if upload_file.is_valid():
            # Save file.
            saved_file = upload_file.save()

            # Update Target model.
            target.name = request.FILES['file_model']
            target.x_train = request.FILES['file_x_train']
            target.y_train = request.FILES['file_y_train']
            target.x_test = request.FILES['file_x_test']
            target.y_test = request.FILES['file_y_test']
            target.overview = request.POST['overview']
            target.author = request.POST['author']
            target.registration_date = saved_file.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')
            target.target_path = os.path.dirname(saved_file.file_model.url)
            target.save()
            messages.success(request, 'Upload new model: {}'.format(target.name))
            return redirect('atd:target_list')
    else:
        form = TargetRegistrationForm()
    return render(request, 'atd/modelform_upload.html', {'form': form, 'target': target})


# Upload files.
def modelform_reupload(request, target_id=None):
    if target_id:
        target = get_object_or_404(Target, pk=target_id)
    else:
        return redirect('atd:target_list')

    if request.method == 'POST':
        upload_file = TargetUpdateForm(request.POST, request.FILES)
        if upload_file.is_valid():
            # Save file.
            saved_file = upload_file.save()

            # Move new model and remove old model.
            try:
                # Move new file to target directory.
                print(saved_file.file_model.path + '\n' + '.' + target.target_path)
                shutil.move(saved_file.file_model.path, '.' + target.target_path)
                os.remove(os.path.join('.' + target.target_path, target.name))
            except FileExistsError:
                # Overwrite.
                shutil.move(saved_file.file_model.path, '.' + os.path.join(target.target_path, target.name))
            except Exception as e:
                # Overwrite.
                shutil.move(saved_file.file_model.path, '.' + os.path.join(target.target_path, target.name))
            finally:
                shutil.rmtree(os.path.dirname(saved_file.file_model.path))

            # Update Target model.
            target.name = request.FILES['file_model']
            target.registration_date = saved_file.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')
            target.save()
            messages.success(request, 'Re-Upload new model: {}'.format(target.name))
            return redirect('atd:target_list')
    else:
        form = TargetUpdateForm()
    return render(request, 'atd/modelform_reupload.html', {'form': form, 'target': target})


# Get Dashboard items.
def get_dashboard_items():
    rank_count = {'critical': 0, 'weak': 0, 'normal': 0, 'secure': 0}
    weak_point = {'data_poisoning': 0, 'model_poisoning': 0, 'evasion': 0, 'exfiltration': 0}
    scan_num = {'num': 0, 'latest_date': 'N/A'}

    # Get "Target Num" and "Rank Count".
    targets = Target.objects.all().order_by('id')
    if len(targets) != 0:
        for target in targets:
            if target.status == 'Done':
                # Update "Rank Count".
                if target.rank == 'Critical':
                    rank_count['critical'] += 1
                elif target.rank == 'Weak':
                    rank_count['weak'] += 1
                elif target.rank == 'Normal':
                    rank_count['normal'] += 1
                elif target.rank == 'Secure':
                    rank_count['secure'] += 1

                # Update "Weak Point".
                _, dp_worst_count, mp_worst_count, ev_worst_count, ex_worst_count = get_worst_rank(target.id)
                weak_point['data_poisoning'] += dp_worst_count
                weak_point['model_poisoning'] += mp_worst_count
                weak_point['evasion'] += ev_worst_count
                weak_point['exfiltration'] += ex_worst_count

    # Get "Scan Num".
    results = ScanResult.objects.order_by('id')
    for result in results:
        ext_result = ExtScanResult.objects.db_manager('atd').filter(scan_id__exact=result.scan_id)
        if len(ext_result) == 0:
            continue
        if ext_result[0].status == 'Done':
            scan_num['num'] += 1
            scan_num['latest_date'] = ext_result[0].exec_end_date

    return rank_count, weak_point, scan_num


# Count worst rank.
def count_worst_count(target_id, worst_rank, method_list):
    utility = Utilty()
    worst_count = 0
    for attack_method in method_list:
        result = ExtScanResult.objects.db_manager('atd').filter(target_id__exact=target_id,
                                                                status__exact='Done',
                                                                attack_method__exact=attack_method).reverse().first()
        if result is None:
            continue

        if utility.transform_rank_to_number(result.rank) > worst_rank:
            worst_rank = utility.transform_rank_to_number(result.rank)
        if utility.transform_rank_to_number(result.rank) >= utility.transform_rank_to_number('Weak'):
            worst_count += 1
    return worst_rank, worst_count


# Get worst rank per target.
def get_worst_rank(target_id):
    rank_list = ['Secure', 'Normal', 'Weak', 'Critical']
    worst_rank = 0

    # Data Poisoning.
    worst_rank, dp_worst_count = count_worst_count(target_id, worst_rank, ['feature_collision',
                                                                           'convex_polytope',
                                                                           'bullseye_polytope'])

    # Model Poisoning.
    worst_rank, mp_worst_count = count_worst_count(target_id, worst_rank, ['node_injection',
                                                                           'layer_injection'])

    # Evasion.
    worst_rank, ev_worst_count = count_worst_count(target_id, worst_rank, ['fgsm', 'cnw', 'jsma'])

    # Evasion.
    worst_rank, ex_worst_count = count_worst_count(target_id, worst_rank, ['membership_inference',
                                                                           'label_only',
                                                                           'inversion'])

    return rank_list[worst_rank], dp_worst_count, mp_worst_count, ev_worst_count, ex_worst_count


# Update target's information.
def update_target(targets):
    for target in targets:
        result = ScanResult.objects.filter(scan_result__exact=target.id).order_by('id').reverse().first()
        if result is None:
            continue

        ext_result = ExtScanResult.objects.db_manager('atd').filter(scan_id__exact=result.scan_id)
        if len(ext_result) == 0:
            continue

        # Get worst rank for target.
        worst_rank, _, _, _, _ = get_worst_rank(target.id)
        target.rank = worst_rank

        if ext_result[0].status == 'Done':
            target.accuracy = ext_result[0].accuracy
            target.last_scan_date = ext_result[0].exec_end_date
            target.status = ext_result[0].status
            target.save()

    return targets


# Top Page (Dashboard).
def top_page(request):
    # Get "Target List".
    targets = Target.objects.all().order_by('id')
    targets = update_target(targets)

    rank_count, weak_point, scan_num = get_dashboard_items()
    return render(request, 'atd/index.html', {'rank_count': rank_count,
                                              'weak_point': weak_point,
                                              'scan_num': scan_num,
                                              'targets': targets})


# Target list.
def target_list(request):
    targets = Target.objects.all().order_by('id')
    targets = update_target(targets)
    return render(request, 'atd/target_list.html', {'targets': targets})


# Edit Target's information.
def target_edit(request, target_id=None):
    if target_id:
        target = get_object_or_404(Target, pk=target_id)
    else:
        target = Target()

    if request.method == 'POST':
        form = TargetForm(request.POST, request.FILES, instance=target)
        if form.is_valid():
            target = form.save(commit=False)
            target.save()
            messages.success(request, 'Update target\'s information: {}.{}'.format(target_id, target.name))
            return redirect('atd:target_list')
    else:
        form = TargetForm(instance=target)

    return render(request, 'atd/target_edit.html', dict(target=target, form=form, target_id=target_id))


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
            result = ExtEvasionFGSM.objects.filter(target_id__exact=target_id)
            if len(result) == 0:
                setting_form = FGSMSettingForm()
            else:
                setting_form = FGSMSettingForm(instance=result[0])
        elif request.POST['method'] == 'evasion_cnw':
            attack_method = utility.transform_attack_method_name(request.POST['method'])
            result = ExtEvasionCnW.objects.filter(target_id__exact=target_id)
            if len(result) == 0:
                setting_form = CnWSettingForm()
            else:
                setting_form = CnWSettingForm(instance=result[0])
        elif request.POST['method'] == 'evasion_jsma':
            attack_method = utility.transform_attack_method_name(request.POST['method'])
            result = ExtEvasionJSMA.objects.filter(target_id__exact=target_id)
            if len(result) == 0:
                setting_form = JSMASettingForm()
            else:
                setting_form = JSMASettingForm(instance=result[0])
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
                                      epsilon=params['epsilon'],
                                      epsilon_step=params['epsilon_step'],
                                      targeted=targeted,
                                      batch_size=params['batch_size'],
                                      dataset_num=params['dataset_num'])
        fgsm_setting.save()
        messages.success(request, 'Update scan setting: {}'.format(params['attack_id']))
    # Insert/Update EvasionCnWTBL
    elif params['attack_id'] == 'evasion_cnw':
        cnw_setting = ExtEvasionCnW(target_id=target_id,
                                    confidence=params['confidence'],
                                    batch_size=params['batch_size'],
                                    dataset_num=params['dataset_num'])
        cnw_setting.save()
        messages.success(request, 'Update scan setting: {}'.format(params['attack_id']))
    # Insert/Update EvasionJSMATBL
    elif params['attack_id'] == 'evasion_jsma':
        jsma_setting = ExtEvasionJSMA(target_id=target_id,
                                      theta=params['theta'],
                                      gamma=params['gamma'],
                                      batch_size=params['batch_size'],
                                      dataset_num=params['dataset_num'])
        jsma_setting.save()
        messages.success(request, 'Update scan setting: {}'.format(params['attack_id']))
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
    model_path = '.' + os.path.join(target.target_path, target.name)
    x_train_path = '.' + os.path.join(target.target_path, target.x_train)
    y_train_path = '.' + os.path.join(target.target_path, target.y_train)
    x_test_path = '.' + os.path.join(target.target_path, target.x_test)
    y_test_path = '.' + os.path.join(target.target_path, target.y_test)
    common = '--target_id {} --scan_id {} --op_type attack --model_name {}'.format(target.id, scan_id, model_path)
    common_test_data = '--test_data_name {} --test_label_name {}'.format(x_test_path, y_test_path)

    # Build attack's parameters.
    # FGSM.
    if params['method'] == 'evasion_fgsm':
        specify_option = ' --attack_type evasion --attack_evasion fgsm'
        fgsm_setting = ExtEvasionFGSM.objects.filter(target_id__exact=target.id)
        if len(fgsm_setting) != 0:
            # Setting of DB.
            specify_option += ' --use_x_test_num {}'.format(fgsm_setting[0].dataset_num)
            specify_option += ' --fgsm_epsilon {}'.format(fgsm_setting[0].epsilon)
            specify_option += ' --fgsm_eps_step {}'.format(fgsm_setting[0].epsilon_step)
            if fgsm_setting[0].targeted == True:
                specify_option += ' --fgsm_targeted'
            specify_option += ' --fgsm_batch_size {}'.format(fgsm_setting[0].batch_size)
        else:
            # Default setting.
            fgsm_setting = ScanSettingFGSM()
            specify_option += ' --use_x_test_num {}'.format(fgsm_setting.dataset_num)
            specify_option += ' --fgsm_epsilon {}'.format(fgsm_setting.epsilon)
            specify_option += ' --fgsm_eps_step {}'.format(fgsm_setting.epsilon_step)
            specify_option += ' --fgsm_batch_size {}'.format(fgsm_setting.batch_size)
    # CnW.
    elif params['method'] == 'evasion_cnw':
        specify_option = ' --attack_type evasion --attack_evasion cnw'
        cnw_setting = ExtEvasionCnW.objects.filter(target_id__exact=target.id)
        if len(cnw_setting) != 0:
            # Setting of DB.
            specify_option += ' --use_x_test_num {}'.format(cnw_setting[0].dataset_num)
            specify_option += ' --cnw_confidence {}'.format(cnw_setting[0].confidence)
            specify_option += ' --cnw_batch_size {}'.format(cnw_setting[0].batch_size)
        else:
            # Default setting.
            cnw_setting = ScanSettingCnW()
            specify_option += ' --use_x_test_num {}'.format(cnw_setting.dataset_num)
            specify_option += ' --cnw_confidence {}'.format(cnw_setting.confidence)
            specify_option += ' --cnw_batch_size {}'.format(cnw_setting.batch_size)
    # JSMA.
    elif params['method'] == 'evasion_jsma':
        specify_option = '--use_x_test_num 100 --attack_type evasion --attack_evasion jsma'
        jsma_setting = ExtEvasionJSMA.objects.filter(target_id__exact=target.id)
        if len(jsma_setting) != 0:
            # Setting of DB.
            specify_option += ' --use_x_test_num {}'.format(jsma_setting[0].dataset_num)
            specify_option += ' --jsma_theta {}'.format(jsma_setting[0].theta)
            specify_option += ' --jsma_gamma {}'.format(jsma_setting[0].gamma)
            specify_option += ' --jsma_batch_size {}'.format(jsma_setting[0].batch_size)
        else:
            # Default setting.
            jsma_setting = ScanSettingJSMA()
            specify_option += ' --use_x_test_num {}'.format(jsma_setting.dataset_num)
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
        messages.error(request, 'Target ID is invalid: "{}" ?'.format(target_id))
        return redirect('atd:target_list')

    # Existing check of model and dataset.
    if os.path.exists('.' + os.path.join(target.target_path, target.name)) is False:
        messages.warning(request, 'Target model file is not found: "{}" ?'.format(target.name))
    elif os.path.exists('.' + os.path.join(target.target_path, target.x_train)) is False:
        messages.warning(request, 'X_train file is not found: "{}" ?'.format(target.x_train))
    elif os.path.exists('.' + os.path.join(target.target_path, target.y_train)) is False:
        messages.warning(request, 'y_train file is not found: "{}" ?'.format(target.y_train))
    elif os.path.exists('.' + os.path.join(target.target_path, target.x_test)) is False:
        messages.warning(request, 'X_test file is not found: "{}" ?'.format(target.x_test))
    elif os.path.exists('.' + os.path.join(target.target_path, target.y_test)) is False:
        messages.warning(request, 'y_test file is not found: "{}" ?'.format(target.y_test))
    else:
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
        messages.success(request, 'Execute {} for "{}"'.format(utility.transform_attack_method_name(request.POST['method']),
                                                               target.name))

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
    messages.success(request, 'Delete target "{}.{}"'.format(target_id, target.name))
    return redirect('atd:target_list')

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django_celery_results.models import TaskResult
from celery.result import AsyncResult

from gyoiboard.tasks import executation
from atd.models import Target, ScanResult
from atd.forms import UploadFileForm, TargetForm, ScanResultForm, FGSMSettingForm


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
    if target_id:
        # Select Attack Method's form.
        attack_method = ''
        if request.POST['tags'] == 'evasion_fgsm':
            attack_method = 'Fast Gradient Signed Method'
            setting_form = FGSMSettingForm()
        else:
            # TODO: 他の攻撃手法のフォームを用意すること。
            attack_method = 'Fast Gradient Signed Method'
            setting_form = FGSMSettingForm()
    else:
        return redirect('atd:target_list')

    return render(request, 'atd/scan_setting.html', dict(form=setting_form,
                                                         target_id=target_id,
                                                         attack_method=attack_method))


# Scan Execution.
def scan_exec(request, target_id):
    if target_id:
        target = get_object_or_404(Target, pk=target_id)
    else:
        return redirect('atd:target_list')

    # Execution.
    task = executation.delay('python3 /home/itakaesu/PycharmProjects/Adversarial-Threat-Detector/atd.py -h')
    print(task.id)
    task_1 = AsyncResult(task.id)
    print(task_1.status)

    result = list(TaskResult.objects.filter(task_id=task.id).values_list('result', flat=True))
    if len(result) == 0:
        result[0] = 'Could not execute.'
    context = {'result': result[0].encode('utf-8')}

    return render(request, 'atd/scan_exec.html', dict(context))


# Execute fix.
def target_fix(request, target_id):
    return


# Delete Target's information.
def target_del(request, target_id):
    target = get_object_or_404(Target, pk=target_id)
    target.delete()
    return redirect('atd:target_list')


# Edit scan result.
def scan_result_edit(request, target_id, scan_result_id=None):
    target = get_object_or_404(Target, pk=target_id)
    if scan_result_id:
        scan_result = get_object_or_404(ScanResult, pk=scan_result_id)
    else:
        scan_result = ScanResult()

    if request.method == 'POST':
        form = ScanResultForm(request.POST, instance=scan_result)
        if form.is_valid():
            scan_result = form.save(commit=False)
            scan_result.target = target
            scan_result.save()
            return redirect('atd:scan_result_list', target_id=target_id)
    else:
        form = ScanResultForm(instance=scan_result)

    return render(request,
                  'atd/scan_result_edit.html',
                  dict(form=form, target_id=target_id, scan_result_id=scan_result_id))


# Delete scan result.
def scan_result_del(request, target_id, scan_result_id):
    scan_result = get_object_or_404(ScanResult, pk=scan_result_id)
    scan_result.delete()
    return redirect('atd:scan_result_list', target_id=target_id)


class ScanResultList(ListView):
    # Scan's results.
    context_object_name = 'scan_result'
    template_name = 'atd/scan_result_list.html'
    paginate_by = 2

    def get(self, request, *args, **kwargs):
        target = get_object_or_404(Target, pk=kwargs['target_id'])
        scan_results = target.impressions.all().order_by('id')
        self.object_list = scan_results

        context = self.get_context_data(object_list=self.object_list, target=target)
        return self.render_to_response(context)

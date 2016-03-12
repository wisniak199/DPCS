from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from alpha.models import Application, SystemInfo, CrashGroup, CrashReport, Solution
from alpha.serializers import ApplicationSerializer, CrashGroupSerializer, CrashReportSerializer, SystemInfoSerializer, SolutionSerializer

# Adds the crash report to the database. Returns crash report's id on success. Otherwise returns -1
def add_crash_report(request):
    reports = CrashReport.objects.all()
    if(request.method=='POST'):
        cr_id = int(request.data['crash_report_id'])
        cg_id = int(request.data['crash_group_id'])
        std_err = request.data['stderr_output']
        ex_code = int(request.data['exit_code'])
        ap = request.data['application']
        sysinfo = request.data['systeminfo']

        try:
            cr = CrashReport.objects.get(pk=cr_id)
            return -1
        except CrashReport.DoesNotExist:
            pass

        try:
            cg = CrashGroup.objects.get(crash_group_id=cg_id)
        except CrashGroup.DoesNotExist:
            cg = CrashGroup(crash_group_id=cg_id)
            cg.save()

        try:
            app = Application.objects.get(version=ap["version"])
        except Application.DoesNotExist:
            app = Application(version=ap["version"])
            app.save()

        try:
            system = SystemInfo.objects.get(version=sysinfo["version"])
        except SystemInfo.DoesNotExist:
            system = SystemInfo(version=sysinfo["version"])
            system.save()

        new_crash_report = CrashReport(crash_report_id=cr_id, crash_group_id=cg, stderr_output=std_err, exit_code=ex_code, application=app, systeminfo=system)
        new_crash_report.save()
        return cr_id
    return -1

def add_solution(request):
    if(request.method=='POST'):
        sol_id = int(request.data['solution_id'])
        cg_id = int(request.data['crash_group_id'])
        shellscript = request.data['shell_script']

        try:
            sol = Solution.objects.get(pk=sol_id)
            return -1
        except Solution.DoesNotExist:
            pass

        cg = {}
        try:
            cg = CrashGroup.objects.get(pk=cg_id)
        except CrashGroup.DoesNotExist:
            return -1

        new_sol = Solution(solution_id=sol_id, crash_group_id=cg, shell_script = shellscript)
        new_sol.save()
        return sol_id
    return -1

@api_view(['GET', 'POST'])
def crash_group_list(request):
    """
    List all crash groups, or create a new one.
    """
    if request.method == 'GET':
        snippets = CrashGroup.objects.all()
        serializer = CrashGroupSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        #serializer = CrashGroupSerializer(data=request.data)
        serializer = CrashGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def crash_group_detail(request, pk):
    """
    Retrieve, update or delete a snippet instance.
    """
    try:
        group = CrashGroup.objects.get(pk=pk)
    except CrashGroup.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CrashGroupSerializer(group)
        return Response(serializer.data)

    # elif request.method == 'PUT':
    #     serializer = CrashGroupSerializer(group, data=request.data)
    #     cgrp_id = request.data["crash_group_id"]
    #
    #     print(serializer.is_valid())
    #     print(request.data)
    #     print("Changing group id from " + pk + " to ... " + cgrp_id)
    #     #print(serializer)
    #     if serializer.is_valid():
    #         serializer.save()
    #         to_delete = CrashGroup.objects.get(pk=pk)
    #         to_delete.delete()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def crash_report_list(request):
    """
    List all crash reports, or create a new one.
    """
    if request.method == 'GET':
        reports = CrashReport.objects.all()
        serializer = CrashReportSerializer(reports, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print("POST report list")
        added = add_crash_report(request)
        print(added)
        if added == -1:
            return Response("Could not add the crash report ... Make sure you passed correct arguments ...",
                            status=status.HTTP_400_BAD_REQUEST)
        #serializer = CrashReportSerializer(crash_report_id=added)
        try:
            report = CrashReport.objects.get(pk=added)
        except CrashReport.DoesNotExist:
            return Response("Could not add the crash report ... Make sure you passed correct arguments ...",
                status=status.HTTP_400_BAD_REQUEST)

        serializer = CrashReportSerializer(report)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


        #serializer = CrashReportSerializer(data=request.data)
        #print(serializer.is_valid())
        #print(serializer)
        #x = request.data["crash_report_id"]
        #print(x)
        #if serializer.is_valid():
        #    serializer.save()
        #    return Response(serializer.data, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def crash_report_detail(request, pk):
    """
    Retrieve, update or delete a crash report
    """
    print("Crash report detail ...")


    try:
        report = CrashReport.objects.get(pk=pk)
    except CrashReport.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CrashReportSerializer(report)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CrashReportSerializer(report, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        report.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def crash_group_add(request):
    groups = CrashGroup.objects.all()
    if(request.method=='GET'):
        return render_to_response('alpha/crash_group_add.html', {'groups': groups}, context_instance=RequestContext(request))
    if(request.method=='POST'):
        crash_grp_id = request.POST.get('crash_group_id')
        try:
            crash_grp = CrashGroup.objects.get(crash_group_id=crash_grp_id)
            return render_to_response('alpha/crash_group_add.html', {'groups': groups, 'msg': "This crash_group is already in database."},
            context_instance=RequestContext(request))
        except CrashGroup.DoesNotExist:
            new_crash_grp = CrashGroup(crash_group_id=crash_grp_id)
            new_crash_grp.save()
            return render_to_response('alpha/crash_group_add.html', {'groups': groups, 'msg': "Saved new crash_grp"},
            context_instance=RequestContext(request))

def crash_report_add(request):
    reports = CrashReport.objects.all()
    if(request.method == 'GET'):
        return render_to_response('alpha/crash_report_add.html', {'reports': reports}, context_instance=RequestContext(request))
    elif(request.method=='POST'):
        cr_id = int(request.POST.get('crash_report_id'))
        cg_id = int(request.POST.get('crash_group_id'))
        std_err = request.POST.get('stderr_output')
        ex_code = int(request.POST.get('exit_code'))
        app_name = request.POST.get('application_name')
        app_v = request.POST.get('application_version')
        sys_ver = request.POST.get('system_version')

        app = {}
        system = {}

        try:
            cg = CrashGroup.objects.get(crash_group_id=cg_id)
        except CrashGroup.DoesNotExist:
            cg = CrashGroup(crash_group_id=cg_id)
            cg.save()
        try:
            app = Application.objects.get(name=app_name, version=app_v)
        except Application.DoesNotExist:
            app = Application(name=app_name, version=app_v)
            app.save()

        try:
            system = SystemInfo.objects.get(version=sys_ver)
        except SystemInfo.DoesNotExist:
            system = SystemInfo(version=sys_ver)
            system.save()

        new_crash_report = CrashReport(crash_report_id=cr_id, crash_group_id=cg, stderr_output=std_err, exit_code=ex_code, application=app, systeminfo=system)
        new_crash_report.save()

        return render_to_response('alpha/crash_report_add.html', {'reports': reports}, context_instance=RequestContext(request))

@api_view(['GET', 'PUT', 'DELETE'])
def solution_detail(request, pk):
    try:
        sol = Solution.objects.get(pk=pk)
    except Solution.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SolutionSerializer(sol)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = SolutionSerializer(sol, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        sol.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST', 'GET'])
def solution_list(request):
    if request.method == 'POST':
        new_sol_id = add_solution(request)
        if new_sol_id == -1:
            return Response("Could not add the solution ... Make sure you passed correct arguments ...",
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            sol = Solution.objects.get(pk=new_sol_id)
        except Solution.DoesNotExist:
            return Response("Could not add the crash report ... Make sure you passed correct arguments ...",
                status=status.HTTP_400_BAD_REQUEST)

        serializer = SolutionSerializer(sol)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        solutions = Solution.objects.all()
        serializer = SolutionSerializer(solutions, many=True)
        return Response(serializer.data)
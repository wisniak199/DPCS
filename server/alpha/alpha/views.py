from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from alpha.models import Application, SystemInfo, \
    CrashGroup, CrashReport, Solution
from alpha.serializers import CrashGroupSerializer, \
    CrashReportSerializer, SolutionSerializer


crash_reports_url = 'vd1/crash-reports/'
crash_groups_url = 'vd1/crash-groups/'
solutions_url = 'vd1/solutions/'


# Adds the crash report to the database. Returns crash report's id on success.
# Otherwise returns -1
def add_crash_report(request):
    if request.method == 'POST':
        # assume the data is passed correctly ...
        std_err = request.data['crash_report']['stderr_output']
        ex_code = int(request.data['crash_report']['exit_code'])
        sysinfo = request.data['crash_report']['system_info']
        application = request.data['crash_report']['application']

        ############################### OPTION 2: ADDED PLATFORM & PACKAGES FIELD TO SYSTEMINFO model ######################################
        # try:
        #     system = SystemInfo.objects.get(platform=sysinfo["platform"],
        #                                     packages=sysinfo["packages"],
        #                                     version=sysinfo["version"])
        # except SystemInfo.DoesNotExist:
        #     system = SystemInfo(platform=sysinfo["platform"],
        #                         packages=sysinfo["packages"],
        #                         version=sysinfo["version"])
        #    system.save()

        try:
            system = SystemInfo.objects.get(version=sysinfo["version"])
        except SystemInfo.DoesNotExist:
            system = SystemInfo(version=sysinfo["version"])
            system.save()

        try:
            app = Application.objects.get(name=application["name"],
                                          version=application["version"])
        except Application.DoesNotExist:
            app = Application(name=application["name"],
                              version=application["version"])
            app.save()

        new_crash_report = CrashReport(
            stderr_output=std_err, exit_code=ex_code,
            system_info=system, application=app
        )

        new_crash_report.save()
        return new_crash_report.crash_report_id
    return -1


# Adds the solution to the database. Returns solution's id on success.
# Otherwise returns -1
def add_solution(request):
    if request.method == 'POST':

        # assume the data is passed correctly ...
        cg_id = int(request.data['solution']['crash_group_id'])
        shellscript = request.data['solution']['shell_script']
        try:
            cg = CrashGroup.objects.get(pk=cg_id)
            new_sol = Solution(
                crash_group_id=cg,
                shell_script=shellscript
            )
            new_sol.save()
            return new_sol.solution_id
        except CrashGroup.DoesNotExist:
            return -1

    return -1


# list all crash groups or create a new one
@api_view(['GET', 'PUT'])
def crash_group_list(request):
    if request.method == 'GET':
        crash_grp_list = CrashGroup.objects.all()
        serializer = CrashGroupSerializer(crash_grp_list, many=True)
        return Response(serializer.data)

    elif request.method == 'PUT':
        new_crash_grp = CrashGroup()
        new_crash_grp.save()
        json_resp = {}
        json_resp["crash_group_id"] = new_crash_grp.crash_group_id
        json_resp["crash_group_url"] = crash_groups_url + str(new_crash_grp.crash_group_id)
        return Response(json_resp, status=status.HTTP_200_OK)


# view responsible for listing or deleting a crash group
@api_view(['GET', 'PUT', 'DELETE'])
def crash_group_detail(request, pk):
    try:
        group = CrashGroup.objects.get(pk=pk)
    except CrashGroup.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        json_resp = {}
        json_resp["crash_group_id"] = group.crash_group_id
        json_resp["crash_group_url"] = crash_groups_url + str(pk)
        return Response(json_resp, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        group.delete()
        return Response(status=status.HTTP_200_OK)


# view, responsible for listing all the crash reports and dealing
# with HTTP requests to create a crash report
@api_view(['GET', 'POST'])
def crash_report_list(request):
    if request.method == 'GET':
        reports = CrashReport.objects.all()
        serializer = CrashReportSerializer(reports, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        added = add_crash_report(request)
        if added == -1:
            return Response(
                "Could not add the crash report ..."
                "Make sure you passed correct arguments ...",
                status=status.HTTP_400_BAD_REQUEST
            )
        report = CrashReport.objects.get(pk=added)
        json_resp = {}
        json_resp["crash_report_ack"] = {}
        json_resp["crash_report_ack"]["crash_report_id"] = added
        json_resp["crash_report_ack"]["crash_report_url"] = crash_reports_url + str(added)
        json_resp["crash_report_ack"]["crash_group_id"] = report.crash_group_id
        json_resp["crash_report_ack"]["crash_group_url"] = crash_groups_url + str(report.crash_group_id)

        # Since at the time of adding a report we can't know the solution to the problem, we can write the following:
        json_resp["crash_report_ack"]["solution"] = {}
        json_resp["crash_report_ack"]["solution"]["solution_id"] = None
        json_resp["crash_report_ack"]["solution"]["solution_url"] = None
        json_resp["crash_report_ack"]["solution"]["shell_script"] = None
        # http://docs.dpcs.apiary.io/#reference/crashes/crash-report-collection/send-a-new-report
        return Response(json_resp, status=status.HTTP_201_CREATED)


# view responsible for either: listing information on a specific crash report,
# changing a specific crash report or deleting it
@api_view(['GET', 'PUT', 'DELETE'])
def crash_report_detail(request, pk):
    try:
        report = CrashReport.objects.get(pk=pk)
    except CrashReport.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CrashReportSerializer(report)
        json_resp = {}
        json_resp["crash_report"] = serializer.data
        json_resp["crash_report"]["crash_report_url"] = crash_reports_url + str(pk)
        json_resp["crash_report"]["crash_group_url"] = crash_groups_url + str(report.crash_group_id)
        return Response(json_resp, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = CrashReportSerializer(report, request.data['crash_report'], partial=True)
        if serializer.is_valid():
            serializer.save()
            # by now we have updated unnested fields.
            # Now we have to update nested ones(application, system_info)
            sysinfo_obj = request.data['crash_report'].get('system_info', None)
            app_obj = request.data['crash_report'].get('application', None)
            if app_obj:
                try:
                    app = Application.objects.get(
                        name=request.data['crash_report']['application']['name'],
                        version=request.data['crash_report']['application']['version']
                    )
                except Application.DoesNotExist:
                    app = Application(
                        name=request.data["crash_report"]["application"]["name"],
                        version=request.data["crash_report"]["application"]["version"]
                    )
                    app.save()
                report.application = app

            #################### OPTION 2: possibly we have to change this to have compatibility with package & platform field ##############################
            if sysinfo_obj:
                try:
                    sysinfo = SystemInfo.objects.get(version=request.data["crash_report"]["system_info"]["version"])
                except SystemInfo.DoesNotExist:
                    sysinfo = SystemInfo(version=request.data["crash_report"]["system_info"]["version"])
                    sysinfo.save()
                report.system_info = sysinfo
            report.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        report.delete()
        return Response(status=status.HTTP_200_OK)


# view for displaying info about a solution, adding a solution or deleting it
@api_view(['GET', 'PUT', 'DELETE'])
def solution_detail(request, pk):
    try:
        sol = Solution.objects.get(pk=pk)
    except Solution.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SolutionSerializer(sol)
        json_resp = {}
        json_resp["solution"] = serializer.data
        json_resp["solution"]["solution_url"] = solutions_url + str(sol.solution_id)
        json_resp["solution"]["crash_group_url"] = crash_groups_url + str(sol.crash_group_id)
        return Response(json_resp, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = SolutionSerializer(sol, request.data["solution"], partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    elif request.method == 'DELETE':
        sol.delete()
        return Response(status=status.HTTP_200_OK)


# view used for listing all the solutions or adding a new one
@api_view(['POST', 'GET'])
def solution_list(request):
    if request.method == 'POST':
        new_sol_id = add_solution(request)
        if new_sol_id == -1:
            return Response(
                "Could not add the solution ..."
                "Make sure you passed correct arguments ...",
                status=status.HTTP_400_BAD_REQUEST
            )
        sol = Solution.objects.get(pk=new_sol_id)
        json_resp = {}
        json_resp["solution_ack"] = {}
        json_resp["solution_ack"]["solution_id"] = sol.solution_id
        json_resp["solution_ack"]["solution_url"] = solutions_url + str(sol.solution_id)
        return Response(json_resp, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        solutions = Solution.objects.all()
        serializer = SolutionSerializer(solutions, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def paths(request):
    json_resp = {"crash-reports": crash_reports_url, "crash-groups": crash_groups_url, "solutions": solutions_url}
    return Response(json_resp, status=status.HTTP_200_OK)

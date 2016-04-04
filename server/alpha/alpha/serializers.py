from rest_framework import serializers
from alpha.models import SystemInfo, CrashReport
from alpha.models import CrashGroup, Application, Solution


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('name', 'version')


class SystemInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemInfo
        fields = ('name', 'packages', 'platform')


class CrashReportSerializer(serializers.ModelSerializer):
    systeminfo = SystemInfoSerializer(read_only=False)

    class Meta:
        model = CrashReport
        fields = ('crash_report_id', 'crash_group_id',
                  'stderr_output', 'exit_code', 'systeminfo')


class CrashGroupSerializer(serializers.ModelSerializer):
    crash_group_reports = CrashReportSerializer(many=True,
                                                required=False, read_only=True)

    class Meta:
        model = CrashGroup
        fields = ('crash_group_id', 'crash_group_reports')

    def create(self, validated_data):
        return CrashGroup.objects.create(**validated_data)


class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ('solution_id',
                  'crash_group_id', 'shell_script')

from django.db import models


class CrashGroup(models.Model):
    crash_group_id = models.AutoField(primary_key=True)

    def __str__(self):
        return str(self.crash_group_id)


class Application(models.Model):
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=255)

    def __str__(self):
        return "Application: " + self.name + " " + self.version + "\n"


class SystemInfo(models.Model):
    name = models.CharField(max_length=255, default="Ubuntu")
    platform = models.CharField(max_length=255)
    packages = models.TextField()

    def __str__(self):
        return "System information: " + self.name + self.version + "\n"


class CrashReport(models.Model):
    crash_report_id = models.AutoField(primary_key=True)
    crash_group_id = models.ForeignKey(CrashGroup, null=True,
                                       related_name='crash_group_reports')
    stderr_output = models.TextField()
    exit_code = models.IntegerField()
    systeminfo = models.ForeignKey(SystemInfo)
    application = models.ForeignKey(Application, null=True)

    def __str__(self):
        text = "Crash report: "
        text += str(self.crash_report_id) + " "
        text += str(self.crash_group_id) + " "
        text += str(self.exit_code) + " "
        text += self.stderr_output + "\n"
        return text


class Solution(models.Model):
    solution_id = models.AutoField(primary_key=True)
    crash_group_id = models.ForeignKey(CrashGroup)
    shell_script = models.TextField()

    def __str__(self):
        text = "Solution: "
        text += str(self.solution_id) + " "
        text += str(self.crash_group_id) + " "
        text += self.shell_script

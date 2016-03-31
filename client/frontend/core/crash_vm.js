function CrashVM(data, root) {
    var self = this;

    self.ReportId = ko.observable(data.crash_report_id || "");
    self.ReportUrl = ko.observable(data.crash_report_url || "");
    self.GroupId = ko.observable(data.crash_group_id || "");
    self.GroupUrl = ko.observable(data.crash_group_url || "");
    self.ExitCode = ko.observable(data.exit_code || "");
    self.StderrOutput = ko.observable(data.stderr_output || "");

    self.Application = ko.observable({
        Name: ko.observable((data.application && data.application.name) || ""),
        Version: ko.observable((data.application && data.application.version) || "")
    });
    self.SystemInfo = ko.observable({
        Version: ko.observable((data.system_info && data.system_info.version) || "")
    });

    //computed
    self.Group = ko.computed(function () {
        return ko.utils.arrayFirst(root.crashGroupsData(), function (group) {
            return group.GroupId() === self.GroupId();
        });
    });

    //functions
    self.Edit = function () {
        alert("edit1");
    }
}
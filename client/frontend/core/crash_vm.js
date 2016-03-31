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
        Name: ko.observable((data.application && data.system_info.name) || ""),
        Version: ko.observable((data.system_info && data.system_info.version) || "")
    });

    //computed
    self.Group = ko.computed(function() {
        return ko.utils.arrayFirst(root.crashGroupsData(), function(group) {
            return group.GroupId() === self.GroupId();
        });
    });

    //functions
    self.Edit = function() {
        alert("edit1");
    }

    //Assigning to CG
    self.NewCrashGroup = ko.observable(self.GroupId());

    self.assignReport = function() {
        var sendObject = {
            "crash_report_id": self.ReportId,
            "crash_group_id": self.NewCrashGroup(),
            "stderr_output": self.StderrOutput(),
            "exit_code": self.ExitCode(),
            "application": {
                "name": self.Application().Name(),
                "version": self.Application().Version()
            },
            "systeminfo": {
                "name": self.SystemInfo().Name(),
                "version": self.SystemInfo().Version()
            }
        }

        $.ajax(Repository.CrashReports.put(self.ReportId(), sendObject))
            .then(function() {
                self.GroupId(self.NewCrashGroup());
            });

    }

    self.ConfirmButtonClass = ko.pureComputed(function() {
        return self.GroupId() == self.NewCrashGroup() ? "btn-default" : "btn-success";
    });

}
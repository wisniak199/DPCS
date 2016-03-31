function SolutionVM(data, root) {
    var self = this;

    self.SolutionId = ko.observable((data.solution_id) ? data.solution_id : "");
    self.SolutionUrl = ko.observable(data.crash_report_url || "");
    self.GroupId = ko.observable(data.crash_group_id || "");
    self.GroupUrl = ko.observable(data.crash_group_url || "");
    self.ShellScript = ko.observable(data.shell_script || "");

    //computed
    self.Group = ko.computed(function () {
        return ko.utils.arrayFirst(root.crashGroupsData(), function (group) {
            return group.GroupId() === self.GroupId();
        });
    });


}
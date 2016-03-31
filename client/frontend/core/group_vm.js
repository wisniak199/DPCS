function GroupVM(data, root) {
    var self = this;

    //property
    self.GroupId = ko.observable(data.crash_group_id || "");
    self.GroupUrl = ko.observable(data.crash_group_url || "");


    //computed
    self.Crashes = ko.computed(function () {
        return Enumerable.From(root.crashReportsData())
            .Where(function (crash) {
                return crash.GroupId() === self.GroupId();
            })
            .ToArray();

    });

    self.Solution = ko.computed(function () {
        return ko.utils.arrayFirst(root.crashSolutionsData(), function (solution) {
            return solution.GroupId() === self.GroupId();
        });
    });

    self.GroupName = ko.pureComputed(function () {
        return "#" +self.GroupId() + " "+ (self.Solution() ? self.Solution().ShellScript() : "no solution");
    });

    self.Count = ko.pureComputed(function () {
        return self.Crashes().length;
    });
}
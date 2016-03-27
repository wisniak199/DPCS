function getCrashGroups() {
    var crashGroups = Repository.CrashGroups;
    var crashReports = Enumerable.From(Repository.CrashReports);
    var solutions = Enumerable.From(Repository.Solutions);

    for (var i = 0; i < crashGroups.length; i++) {
        var cg = crashGroups[i];

        cg.crashReports = crashReports
            .Where(
                function (crash) {
                    return crash.crash_report.crash_group_id === cg.crash_group_id;
                })
            .ToArray();

        cg.hasSolution = solutions
            .Any(
                function (solution) {
                    return solution["solution"]["crash_group_id"] === cg["crash_group_id"];
                });
    }

    return Enumerable.From(crashGroups)
        .Select(
            function (cg) {
                return {
                    id: cg["crash_group_id"],
                    count: cg.crashReports.length,
                    hasSolution: cg.hasSolution
                }
            })
        .ToArray();
}

function getUnassignedReports() {
    var crashReports = Enumerable.From(Repository.CrashReports)
        .Where(
            function (crash) {
                return !crash["crash_report"]["crash_group_id"];
            }
        )
        .Select(
            function (crash) {
                return {
                    id: crash["crash_report"]["crash_report_id"],
                    appName: crash["crash_report"]["application"]["name"],
                    appVersion: crash["crash_report"]["application"]["version"],
                    system: crash["crash_report"]["system_info"]["version"],
                    exit_code: crash["crash_report"]["exit_code"],
                    output: crash["crash_report"]["stderr_output"],
                }
            }
        )
        .ToArray();
    return crashReports;
}

function MainViewModel() {
    var self = this;

    self.crashGroupsData = ko.observableArray(getCrashGroups());

    self.crashReportsData = ko.observableArray(getUnassignedReports());

    self.selectedCrashGroup = ko.observable();

    self.assignReport = function(report){
        var crashGroups = Enumerable.From(Repository.CrashGroups);
        self.selectedId = self.selectedCrashGroup();
        self.crashGroupUrl = crashGroups.First(function (crashGroup) { return crashGroup.crash_group_id == self.selectedId })["crash_group_url"];

        $.ajax({
                url: "http://private-anon-71b931be7-dpcs.apiary-mock.com/vd1/crash-reports/"+report.id,
                type: "GET",
            })
            .done(function (response) {
                response["crash_report"]["crash_group_id"] = self.selectedId
                response["crash_report"]["crash_group_url"] = self.crashGroupUrl
                $.ajax({
                        url: "http://private-anon-71b931be7-dpcs.apiary-mock.com/vd1/crash-reports/"+report.id,
                        type: "PUT",
                        data: {"crash_report": response}
                    })
                    .done(function (response, textStatus, jqXHR) {
                        if(jqXHR.status==200) {
                            self.crashReportsData.remove(report)
                        }
                    });
            });
    }
}
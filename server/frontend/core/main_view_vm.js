function MainViewModel() {
    var self = this;

    self.crashGroupsData = ko.observableArray();
    self.crashReportsData = ko.observableArray();
    self.crashSolutionsData = ko.observableArray();
    
    //load all crash reports
    $.ajax(Repository.CrashReports.all()).done(function (response) {
        var reports = Enumerable.From(response)
            .Select(
                function (crash) {
                    return new CrashVM(crash, self);
                }
            )
            .ToArray();
        ko.utils.arrayPushAll(self.crashReportsData, reports);
    });
    
    self.unassignedCrashReports = ko.pureComputed(function(){
        return Enumerable.From(self.crashReportsData())
            .Where(
                function (crash) {
                    return !crash.GroupId();
                }
            )
            .ToArray();
    })

    //load all crash groups
    $.ajax(Repository.CrashGroups.all())
        .done(function (response) {
            ko.utils.arrayForEach(response, function (cg) {
                self.crashGroupsData.push(new GroupVM(cg, self));
            });
        });


    

    //load all solutions
    $.ajax(Repository.Solutions.all()).done(function (response) {
        var soluions = Enumerable.From(response)
            .Select(
                function (solution) {
                    return new SolutionVM(solution.solution, self);
                }
            )
            .ToArray();
        ko.utils.arrayPushAll(self.crashSolutionsData, soluions);

    });







    //    self.selectedCrashGroup = ko.observable();
    //
    //    self.assignReport = function (report) {
    //        var crashGroups = Enumerable.From(Repository.CrashGroups);
    //        self.selectedId = self.selectedCrashGroup();
    //        self.crashGroupUrl = crashGroups.First(function (crashGroup) {
    //            return crashGroup.crash_group_id == self.selectedId
    //        })["crash_group_url"];
    //
    //        $.ajax({
    //            url: API_URL + "/vd1/crash-reports/" + report.id,
    //            type: "GET",
    //        })
    //            .done(function (response) {
    //                response["crash_report"]["crash_group_id"] = self.selectedId
    //                response["crash_report"]["crash_group_url"] = self.crashGroupUrl
    //                $.ajax({
    //                    url: API_URL + "/vd1/crash-reports/" + report.id,
    //                    type: "PUT",
    //                    data: {
    //                        "crash_report": response
    //                    }
    //                })
    //                    .done(function (response, textStatus, jqXHR) {
    //                        if (jqXHR.status == 200) {
    //                            self.crashReportsData.remove(report)
    //                        }
    //                    });
    //            });
    //    }
    //
        self.CrashToAdd = ko.observable(new CrashVM({}, self));
    
        self.AddCrash = function () {
            self.CrashToAdd(new CrashVM({}, self));
            $('#add-crash-modal').modal('show');
        }
    
        self.SendCrash = function () {
    
            var crashReport = {
                "application": {
                    "name": self.CrashToAdd().Application().Name(),
                    "version": self.CrashToAdd().Application().Version()
                },
                "systeminfo": {
                    "name": self.CrashToAdd().SystemInfo().Name(),
                    "version": self.CrashToAdd().SystemInfo().Version()
                },
                "exit_code": self.CrashToAdd().ExitCode(),
                "stderr_output": self.CrashToAdd().StderrOutput()
            };
    
            $.ajax({
                url: API_URL + "/vd1/crash-reports/",
                type: "POST",
                data: {
                    "crash_report": crashReport
                }
            })
                .done(function (response) {
                    var data = $.extend(crashReport, response.crash_report_ack);
                    self.crashReportsData.push(new CrashVM(data, self));
                    $('#add-crash-modal').modal('hide');
                });
        }
    
        self.SendCrashGroup = function () {
            $.ajax(Repository.CrashGroups.post())
            .done(function (response) {
                var data = response;
                var g = new GroupVM(data, self);
                self.crashGroupsData.push(g);
            });
        }
    
        self.GroupToView = ko.observable(new GroupVM({}, self));
    
        self.ViewCrashGroup = function (group) {
            self.GroupToView(group);
            $('#crash-group-details-modal').modal('show');
        }
}

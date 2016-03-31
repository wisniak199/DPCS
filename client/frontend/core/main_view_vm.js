function MainViewModel() {
    var self = this;

    self.crashGroupsData = ko.observableArray();
    self.crashReportsData = ko.observableArray();
    self.crashSolutionsData = ko.observableArray();


    //load all crash groups
    $.ajax(Repository.CrashReports.all())
        .done(function (response) {
            var cgPromises = Enumerable.From(response)
                .Select(
                    function (crash) {
                        return crash.crash_report.crash_group_id;

                    })
                .Distinct()
                .Select(function (id) {
                    return $.ajax(crashGroups.get(id));
                })
                .ToArray();

            Promise.all(cgPromises)
                .then(function (responses) {
                    ko.utils.arrayForEach(responses, function (response) {
                        self.crashGroupsData.push(new GroupVM(response, self));
                    });
                });
        });


    //load all crash reports
    $.ajax(Repository.CrashReports.all()).done(function (response) {
        var reports = Enumerable.From(response)
            .Select(
                function (crash) {
                    return new CrashVM(crash.crash_report, self);
                }
            )
            .ToArray();
        ko.utils.arrayPushAll(self.crashReportsData, reports);
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
                "system_info": {
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
    
    //    self.SendCrashGroup = function () {
    //
    //        var crashGroup = {
    //
    //        };
    //
    //        $.ajax({
    //            url: "http://private-anon-7dff37ec3-dpcs.apiary-mock.com/vd1/crash-groups",
    //            type: "PUT"
    //        })
    //            .done(function (response) {
    //                var data = response;
    //                var g = new GroupVM(data, self);
    //                self.crashGroupsData.push(g);
    //            });
    //    }
    //
        self.GroupToView = ko.observable(new GroupVM({}, self));
    
        self.ViewCrashGroup = function (group) {
            self.GroupToView(group);
            $('#crash-group-details-modal').modal('show');
        }






    //test data --------------------
        var testGroup = new GroupVM({
            "crash_group_id": 425,
            "crash_group_url": "vd1/crash-groups/425"
        }, self);

        self.crashGroupsData.push(testGroup);

        testGroup = new GroupVM({
            "crash_group_id": 124,
            "crash_group_url": "vd1/crash-groups/124"
        }, self);

        self.crashGroupsData.push(testGroup);

        var testReport = new CrashVM({
            "crash_report_id": 1000,
            "crash_report_url": "vd1/crash-reports/1000",
            "application": {
                "name": "Mozilla firefox",
                "version": "15.0"
            },
            "system_info": {
                "version": "14.04.1 LTS"
            },
            "exit_code": 1,
            "stderr_output": "error: fox overflow"
        }, self);

        self.crashReportsData.push(testReport);
}
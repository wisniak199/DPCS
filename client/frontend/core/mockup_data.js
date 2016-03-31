//from http://docs.dpcs.apiary.io/

// /vd1/crash-reports

var Mock = {
    crashReports: [
        {
            "crash_report": {
                "crash_report_id": 2098,
                "crash_report_url": "vd1/crash-reports/2098",
                "crash_group_id": 123,
                "crash_group_url": "vd1/crash-groups/425",
                "application": {
                    "name": "Google Chrome",
                    "version": "48.0.2564.116"
                },
                "system_info": {
                    "version": "14.04.1 LTS"
                },
                "exit_code": -1,
                "stderr_output": "error: stack overflow"
            }
  },
        {
            "crash_report": {
                "crash_report_id": 2091,
                "crash_report_url": "vd1/crash-reports/2091",
                "crash_group_id": 123,
                "crash_group_url": "vd1/crash-groups/425",
                "application": {
                    "name": "Chromium",
                    "version": "48.0.2564.000"
                },
                "system_info": {
                    "version": "14.04.1 LTS"
                },
                "exit_code": 2,
                "stderr_output": " fatal  error:  stack  overflow"
            }
  },
        {
            "crash_report": {
                "crash_report_id": 2095,
                "crash_report_url": "vd1/crash-reports/2095",
                "crash_group_id": 425,
                "crash_group_url": "vd1/crash-groups/425",
                "application": {
                    "name": "Chromium",
                    "version": "48.0.2564.000"
                },
                "system_info": {
                    "version": "14.04.1 LTS"
                },
                "exit_code": 0,
                "stderr_output": " fatal  error:  stack  overflow"
            }
  },
        {
            "crash_report": {
                "crash_report_id": 298,
                "crash_report_url": "vd1/crash-reports/298",
                "crash_group_id": 223,
                "crash_group_url": "vd1/crash-groups/700",
                "application": {
                    "name": "Chromium",
                    "version": "48.0.2564.000"
                },
                "system_info": {
                    "version": "14.04.1 LTS"
                },
                "exit_code": 404,
                "stderr_output": " fatal  error:  stack  overflow"
            }
  },
        {
            "crash_report": {
                "crash_report_id": 283,
                "crash_report_url": "vd1/crash-reports/28",
                "crash_group_id": 700,
                "crash_group_url": "vd1/crash-groups/700",
                "application": {
                    "name": "Chromium",
                    "version": "48.0.2564.000"
                },
                "system_info": {
                    "version": "14.04.1 LTS"
                },
                "exit_code": -1,
                "stderr_output": " fatal  error:  stack  overflow"
            }
  },
        {
            "crash_report": {
                "crash_report_id": 298,
                "crash_report_url": "vd1/crash-reports/28",
                "application": {
                    "name": "Chromium",
                    "version": "48.0.2564.000"
                },
                "system_info": {
                    "version": "14.04.1 LTS"
                },
                "exit_code": -0,
                "stderr_output": " fatal  error:  stack  overflow"
            }
  },
        {
            "crash_report": {
                "crash_report_id": 284,
                "crash_report_url": "vd1/crash-reports/28",
                "application": {
                    "name": "Chromium",
                    "version": "48.0.2564.000"
                },
                "system_info": {
                    "version": "14.04.1 LTS"
                },
                "exit_code": 44,
                "stderr_output": " fatal  error:  stack  overflow"
            }
  }
],

    // /vd1/crash-groups/crash_group_id
    crashGroups: [
        {
            "crash_group_id": 123,
            "crash_group_url": "vd1/crash-groups/123"
},
        {
            "crash_group_id": 223,
            "crash_group_url": "vd1/crash-groups/223"
},
        {
            "crash_group_id": 998,
            "crash_group_url": "vd1/crash-groups/998"
}
, {
            "crash_group_id": 9699,
            "crash_group_url": "vd1/crash-groups/998"
}],

    // /vd1/solutions/
    solutions: [
        {
            "solution": {
                "solution_id": 461,
                "solution_url": "vd1/solutions/461",
                "crash_group_id": 998,
                "crash_group_url": "vd1/crash-groups/998",
                "shell_script": "# Shell script..."
            }
},
        {
            "solution": {
                "solution_id": 462,
                "solution_url": "vd1/solutions/462",
                "crash_group_id": 998,
                "crash_group_url": "vd1/crash-groups/998",
                "shell_script": "# Shell script..."
            }
},
        {
            "solution": {
                "solution_id": 41,
                "solution_url": "vd1/solutions/41",
                "crash_group_id": 123,
                "crash_group_url": "vd1/crash-groups/123",
                "shell_script": "# Shell script..."
            }
},
        {
            "solution": {
                "solution_id": 61,
                "solution_url": "vd1/solutions/61",
                "crash_group_id": 124,
                "crash_group_url": "vd1/crash-groups/124",
                "shell_script": "# Shell script..."
            }
},
        {
            "solution": {
                "solution_id": 461,
                "solution_url": "vd1/solutions/461",
                "crash_group_id": 124,
                "crash_group_url": "vd1/crash-groups/124",
                "shell_script": "# Modified shell script..."
            }
  }
],
};

var apiary_url = API_URL + "";
var server_url = "http://54.93.105.103:8000";

var API_URL = server_url;

var crashReports = {
    url: API_URL + "/vd1/crash-reports/",

    all: function () {
        return {
            url: this.url,
            type: "GET",
        }
    },

    get: function (id) {
        return {
            url: this.url + id,
            type: "GET",
        }
    },

    getCrashGroupsIds: function () {
        var groupsIds = [];
        $.ajax(this.all())
            .done(function (response) {
                groupsIds = Enumerable.From(response)
                    .Select(
                        function (crash) {
                            return crash.crash_report.crash_group_id;
                        })
                    .ToArray();
                return groupsIds;
            });
    },

    getFor: function (crashGroupId) {
        var crashes = [];
        $.ajax(this.all())
            .done(function (response) {
                crashes = Enumerable.From(response)
                    .Where(
                        function (crash) {
                            return crash.crash_report.crash_report_id === crashGroupId;
                        });
            });
        return crashes;
    },

    put: function (id, data) {
        return {
            url: this.url + id,
            type: "PUT",
            data: data
        }
    },

    post: function (data) {
        return {
            url: this.url,
            type: "POST",
            data: data
        }
    },
};

var crashGroups = {
    url: API_URL + "/vd1/crash-groups/",

    all: function (id) {
        return {
            url: this.url + "?format=json",
            type: "GET",
        };
    },
    get: function (id) {
        return {
            url: this.url + id,
            type: "GET",
        };
    },

    put: function (id, data) {
        return {
            url: this.url + id,
            type: "PUT",
            data: data
        };
    },

    post: function (data) {
        return {
            url: this.url,
            type: "POST",
            data: data
        };
    },
};

var solutions = {
    url: API_URL + "/vd1/solutions/",

    all: function (query) {
        if (!query) {
            query = "";
        }
        return {
            url: this.url + "?search_string=" + query,
            type: "GET",
        }
    },

    get: function (id) {
        return {
            url: this.url + id,
            type: "GET",
        }
    },

    getFor: function (crashGroupId) {
        var solution = null;
        $.ajax(this.all())
            .done(function (response) {
                solution = Enumerable.From(response)
                    .FirstOrDefault(
                        null,
                        function (solution) {
                            return solution.solution.crash_group_id === crashGroupId;
                        });
            });
        return solution;
    },

    put: function (id, data) {
        return {
            url: this.url + id,
            type: "PUT",
            data: data
        }
    },

    post: function (data) {
        return {
            url: this.url,
            type: "POST",
            data: data
        }
    },
};

var Repository = {
    CrashReports: crashReports,
    CrashGroups: crashGroups,
    Solutions: solutions
};
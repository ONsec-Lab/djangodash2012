function Tutorial (config) {
    var self = this;
    self.id = config.id;
    self.currentStep = config.step;
    if (config.enable_editor) {
        self.editor = ace.edit($('.django-ace-widget').get(0).firstChild);
    }
    self.runButton = $('#tutorialRunButton');
    self.viewResultsButton = $('#viewResultsButton');

    if (config.enable_console) {
        self.console = $('#tutorialConsole').jqconsole('Click to the Run button to execute your code\n');
    }

    // if only console
    if (config.enable_console && !config.enable_editor) {
        self.startConsolePrompt();
    }
    self.tutorialNextButton = $('#tutorialNextButton');

    self.runButton.click(function () {
        if (self.runButton.hasClass('disabled')) {
            return false;
        }
        self.console.Write('Executing your code...\n');
        var code = self.editor.getValue();
        self.runButton.addClass('loading');
        self.runButton.addClass('disabled');
        self.sendCode(code);
    });

    self.viewResultsButton.click(function () {
        self.displayResults();
    });
}

Tutorial.prototype.startConsolePrompt = function () {
    var self = this;
    self.console.Prompt(true, self.runConsoleCommand.bind(self));
};

Tutorial.prototype.runConsoleCommand = function (cmd) {
    var self = this;
    var url = self.getStepUrl() + '/console';
    $.ajax(url, {
        type: 'POST',
        dataType: 'json',
        data: {
            cmd: cmd
        },
        success: function (data, status, xhr) {
            self.log(data.results);
            self.startConsolePrompt();
        }
    });
};

Tutorial.prototype.displayResults = function () {
    var self = this;
    $('#resultsWindow').modal('show');
};

Tutorial.prototype.getStepUrl = function () {
    var self = this;
    return '/tutorial/' + self.id + '/' + self.currentStep + '/';
};

Tutorial.prototype.sendCode = function (code) {
    var self = this;
    var data = {
        code: code
    };
    $.ajax(self.getStepUrl() + 'run/', {
        type: 'POST',
        data: JSON.stringify(data),
        dataType: "json",
        success: function (data, textStatus, xhr) {
            self.waitTask(data.task_id, function (data) {
                if (!data.running) {
                    self.whenTaskFinish(data);
                }
            });
        }
    });
};

Tutorial.prototype.log = function (message) {
    var self = this;
    self.console.Write(message, 'jqconsole-output');
};

Tutorial.prototype.waitTask = function (task_id, callback) {
    var self = this;
    getTask(task_id, callback);
};

/**
 * when task finish - check if there any errors,
 * if no display view results and next buttons
 */
Tutorial.prototype.whenTaskFinish = function (task) {
    var self = this;
    self.log(task.results);
    self.runButton.removeClass('loading');
    self.runButton.removeClass('disabled');
    if (task.errors) {
        return displayError('Error, during run your code');
    } else {
        self.viewResultsButton.removeClass('hide');
    }
};

Tutorial.prototype.displayErrors = function (errors) {
    var self = this;
    self.errorsBlock.show();
};
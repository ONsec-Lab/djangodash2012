function Tutorial (config) {
    var self = this;
    self.id = config.id;
    self.currentStep = config.step;
    self.editor = ace.edit($('.django-ace-widget').get(0).firstChild);
    self.runButton = $('#tutorialRunButton');
    self.viewResultsButton = $('#viewResultsButton');
    self.tutorialConsole = $('#tutorialConsole').jqconsole('Click to the Run button to execute your code\n');
    self.runButton.click(function () {
        if (self.runButton.hasClass('disabled')) {
            return false;
        }
        var code = self.editor.getValue();
        self.runButton.addClass('loading');
        self.runButton.addClass('disabled');
        self.sendCode(code);
    });
}

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
            self.waitTask(data.task_id, self.whenTaskFinish.bind(self));
        }
    });
};

Tutorial.prototype.console = function (message) {
    var self = this;
    self.tutorialConsole.Write(message, 'jqconsole-output');
}

Tutorial.prototype.getTask = function (task_id) {
    var self = this;
    $.ajax('/task/' + task_id + '/', {
        type: 'GET',
        dataType: "json",
        success: function (data, textStatus, xhr) {
            if (data.console) {
                self.console(data.console);
            }
            if (!data.running) {
                self.whenTaskFinish(data);
            } else {
                setTimeout(function () {
                    self.getTask(task_id);
                }, 3000);
            }
        }
    });
}

Tutorial.prototype.waitTask = function (task_id) {
    var self = this;
    self.getTask(task_id);
};

/**
 * when task finish - check if there any errors,
 * if no display view results and next buttons
 */
Tutorial.prototype.whenTaskFinish = function (task) {
    var self = this;
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
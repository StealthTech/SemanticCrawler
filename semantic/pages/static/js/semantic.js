const bridge = function(url) {
    window.location.assign(url);
};

const doneHandler = function(message, form) {
    if (message.status === 'ok') {
        let data = form.dataset;
        if (data.lookup === 'login') {

            $('.layout-login').addClass('hidden');
            $('.layout-logout').removeClass('hidden');
            $('#login-modal').modal('hide');

            $('#header-pad-extra-base').load('/api?method=render&shard=header-pad-extra');

        } else if (data.lookup === 'signup') {
            bridge(message.target_url);
        } else if (data.lookup === 'profile') {
            bridge(message.target_url);
        }
    }
};

const failHandler = function(message, form) {
    $('.errors').text('');
    const response = JSON.parse(message.responseText);
    const errors = response.errors;
    const keys = Object.keys(errors);
    keys.forEach(function(item, i, keys) {
        let selector;
        if (item === '__all__') {
            selector = '#id_all_errors';
        } else {
            selector = '#id_' + item + '_errors';
        }
        $(selector).text(errors[item][0]);
    });
};

const submitHandler = function(event) {
    event.preventDefault();
    let form = this;
    let formSettings = {};

    formSettings.formData = new FormData(form);
    formSettings.formUrl = form.action;
    formSettings.contentType = false;

    // console.log(formSettings);

    $.ajax({
        url: formSettings.formUrl,
        type: 'POST',
        cache: false,
        contentType: formSettings.contentType,
        processData: false,
        data: formSettings.formData
    }).done(function(message) {
        doneHandler(message, form);
        // console.log(formSettings);

    }).fail(function (message) {
        failHandler(message, form);
        // console.log(formSettings);

    });
};

const hyperHandler = function(event) {
    event.preventDefault();

    let hyper = this;
    console.log('hyper = ' + hyper);
    let data = hyper.dataset;
    console.log('data = ' + data);

    $.ajax({
        url: '/logout/',
        type: 'GET',
    }).done(function(message) {
        if (message.status === 'ok') {
            console.log('lookup = ' + data.lookup);
            if (data.lookup === 'logout') {
                location.reload();
            }
        }
    }).fail(function(message) {

    });
};

function update_timer(value, map) {
    const repr = seconds_to_repr(value);
    const container = $(map.container);
    const shard = $(map.shard);
    container.text(repr);
    if (value > 0) {
        setTimeout(update_timer, 1000, value - 1, map);
    }
    if (value == 0) {
        shard.load(window.location.href)
    }
}

function seconds_to_repr(value) {
    if (value <= 0) {
        return 'время вышло.';
    }

    const hours = Math.floor(value / 3600);
    const minutes = Math.floor((value % 3600) / 60);
    const seconds = Math.floor(value % 60);

    let result = '';
    if (hours) {
        result += hours + ' ч. ';
    }
    if (minutes) {
        result += minutes + ' мин. ';
    }
    result += seconds + ' сек.';
    return result
}

function check_timers() {
    const timers = [{container: '#record-remaining-time--task', shard: '#task-layout'},
                    {container: '#record-remaining-time--stage', shard: '#stage-layout'}];
    timers.map(function(element) {
        const obj = $(element.container);
        update_timer(parseInt(obj.text()), element);
    });
}

$(document).on('submit', 'form', submitHandler);

$(function() {
    check_timers();
});

$('.hyper').each(function(i, elem) {
   $(this).on('click', hyperHandler)
});


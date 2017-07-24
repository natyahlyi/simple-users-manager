/**
 * Created by andrii on 21.07.17.
 */

function initUserTable() {
    var $table = $('#users-table');
    usersTable = $table.DataTable({
        "drawCallback": resetDelete,
        "ordering": false,
        "bInfo" : false,
        "language": {
            "paginate": {
                "previous": '<i class="glyphicon glyphicon-menu-left"></i>',
                "next": '<i class="glyphicon glyphicon-menu-right"></i>'
            }
        }
    });

    // $('.paginate_button ').on('click', resetDelete());

    function resetDelete() {
        $('.delete-user').off('click');
        setTimeout('lookForDeletes()', 1000)
    }

    function search() {
        var value = $('#search-input').val();
        usersTable
            .columns(0)
            .search(value)
            .draw();
    }
    $('#search-btn').on('click', function () {
        search()
    });

    $(document).keypress(function(e) {
        var focused = $("#search-input").is(":focus");
        if(e.which === 13 && focused) {
            search()
        }
    });


    $('#users_length').change(function () {
        var len = $(this).find(":selected").text();
        usersTable.page.len(len).draw();
    });
}

function lookForDeletes() {
    $('.delete-user').click(function () {
        var id = $(this).data('id');
        var $this = $(this);

        $('.delete-user').off('click');
        $this.off('click');

        deleteUser(id);
    });

}
var csrftoken = $("[name=csrfmiddlewaretoken]").val();

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function deleteUser(id) {
    $.ajax({
        type: 'POST',
        url: '/user/delete',
        data: {'id': id},
        datatype: 'json',
        cache: 'false',
        success: function(data) {
            if (data.status === 'ok'){
                usersTable.row($('#u-' + id)).remove().draw();
                toastr.info('User successfully deleted!', {timeOut: 3000});
            }
        }
    })
}

// listens for courses removes from table and appends them to select
function listenForRemove() {
    $('.remove-course').on('click', function () {
        var c_id = $(this).data('id');
        var $parent = $(this).parent();
        $(this).remove();
        var title = $parent.text();
        $parent.parent().remove();

        var option = $("<option value=\"" + c_id + "\">" + title + "</option>");
        option.appendTo(coursesSelect);
        checkCoursesSelect();
        $('#add-course').off('click');
        listenForAppend()
    });
}

// listens for courses removes from select and appends them to table
function listenForAppend() {
    $('#add-course').on('click', function () {
        var $course = $('#courses');
        var c_id = $course.val();
        var $option = $course.find("option[value='" + c_id + "']");
        var title = $option.text();
        $option.remove();
        var tr = $("<tr><td>" + title + "<span data-id=\"" + c_id +
            "\" class=\"glyphicon glyphicon-remove-circle remove-course\" aria-hidden=\"true\"></span></td></tr>");
        tr.appendTo($memberships);
        checkCoursesSelect();
        $('.remove-course').off('click');
        listenForRemove()
    });
}

// controls courses select visibility
function checkCoursesSelect() {
    var rowCount = $memberships.find('tr').length;
    if (coursesSelect.children('option').length === 0 || rowCount >= 5) {
        $('#select-with-btn').hide()
    } else {
        $('#select-with-btn').show()
    }
}

var errIcon = '<span class="glyphicon glyphicon-info-sign err-icon" aria-hidden="true"></span>';

// options: url, formSelector, msgSuccess, successCallBack, preparationCallBack
function listenForFormSubmit(options) {
    $(document).ready(function () {
        options.formSelector.submit(function (e) {
            e.preventDefault();
            toastr.options = {
                "showDuration": "500",
                "hideDuration": "500",
                "timeOut": "1500",
                "extendedTimeOut": "500"
            };
            if (typeof options.preparationCallBack === 'function'){
                options.preparationCallBack()
            }
            $.ajax({
                method: 'POST',
                data: $(this).serializeArray(),
                url: '' + options.url + '',
                success: function (data) {
                    if (data.status === 'ok'){
                        var $err = $('.err');
                        $err.html('');
                        $err.parent().removeClass('red-text');
                        if (typeof options.msgSuccess !== 'undefined') {
                            toastr.success(options.msgSuccess);
                        }
                        if (typeof options.successCallBack === 'function'){
                            options.successCallBack()
                        }
                    }
                    if (data.status === 'error'){
                        var $err = $('.err');
                        $err.html('');
                        $err.parent().removeClass('red-text');
                        for (var key in data.errors) {

                            var err = data.errors[key];

                            var $target = $('#id_' + key);
                            var $input = $target.parent();
                            $input.addClass('red-text');
                            var $span = $target.next();
                            $span.html(errIcon  + err);
                        }
                    }
                }
            })
        });
    });
}

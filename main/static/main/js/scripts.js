var csrfToken = $('[name="csrfmiddlewaretoken"]').val(); 

    $("#add_new").submit(function(e) {
        e.preventDefault();
        var text = document.getElementById("text").value;
        $.ajax({
            type: "POST",
            url: "/ajax/add_new",
            data: {
                'text': text,
                'csrfmiddlewaretoken': csrfToken,
            },
            success: function() {
                $('#add_new')[0].reset(); //скидываем нашу форму
                $("body").load("http://127.0.0.1:8000/");
            }
        });
    });

    $(".my_class_complete").submit(function(e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: $(this).attr("data-href"),
            data: {
                'csrfmiddlewaretoken': csrfToken,
            },
            success: function() {
               $("body").load("/");
            }
        });
    });

        $(".my_class_delete").submit(function(e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: $(this).attr("data-href"),
            data: {
                'csrfmiddlewaretoken': csrfToken,
            },
            success: function() {
               $("body").load("/");
            }
        });
    });

        $(".my_class_delete_list").submit(function(e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: $(this).attr("data-href"),
            data: {
                'csrfmiddlewaretoken': csrfToken,
            },
            success: function() {
               $("body").load("completed_todos");
            }
        });
    });


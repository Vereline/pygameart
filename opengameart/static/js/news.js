DEFAULT_IMAGE ="/static/user-default.png";

let comment_text = "<li class=\"list-group-item comment\">\n" +
    "                                <div class=\"row\">\n" +
    "                                    <div class=\"col-xs-3 col-xl-3\">\n" +
    "                                        <img src=\"{user_image}\" class=\"rounded-circle img-responsive\" alt=\"\" />\n" +
    "                                    </div>\n" +
    "                                    <div class=\"col-xs-10 col-xl-9\">\n" +
    "                                        <div class=\"date\">\n" +
    "                                            <a href=\"\">Comment Title</a>\n" +
    "                                            <div class=\"mic-info\">\n" +
    "                                                By: <a href=\"#\">{author}</a> {created_date}\n" +
    "                                            </div>\n" +
    "\n" +
    "                                            <div id=\"{comment_pk}\" class=\"comment-text\">{text}</div>\n" +
    "                                                    <button id=\"{comment_pk}\" type=\"button\" class=\"btn btn-primary btn-xs js-update-comment\" title=\"Edit\" data-url=\"{data_url}\">\n" +
    "                                                        Edit\n" +
    "                                                    </button>\n" +
    "                                                    <button id=\"{comment_pk}\" type=\"button\" class=\"btn btn-success btn-xs change approve\" title=\"Approve\">\n" +
    "                                                        Approve\n" +
    "                                                    </button>\n" +
    "                                                    <button id=\"{comment_pk}\" type=\"button\" class=\"btn btn-danger btn-xs change remove\" title=\"Remove\">\n" +
    "                                                        Remove\n" +
    "                                                    </button>\n" +
    "                                        </div>\n" +
    "                                    </div>\n" +
    "                                </div>\n" +
    "                            </li>";

/* Functions */
let loadForm = function () {
  console.log('load');
let btn = $(this);
$.ajax({
  url: btn.attr("data-url"),
  type: 'get',
  dataType: 'json',
  beforeSend: function () {
    $("#modal-comment .modal-content").html("");
    $("#modal-comment").modal("show");
  },
  success: function (data) {
    $("#modal-comment .modal-content").html(data['html_form']);
  }
});
};

let saveForm = function () {
  console.log('save');
let form = $(this);
$.ajax({
  url: form.attr("action"),
  data: form.serialize(),
  type: form.attr("method"),
  dataType: 'json',
  success: function (data) {
    if (data['form_is_valid']) {
      $(".comment-text#"+data['id']).text(data['new_text']);
      $("#modal-comment").modal("hide");
    }
    else {
      $("#modal-comment .modal-content").html(data['html_form']);
    }
  }
});
return false;
};

function createCommentChild(created_date, author, text, may_change, comment_pk, user_image=undefined) {
     let remove_comment_url="/news/comment/remove/"+comment_pk;
     let approve_comment_url="/news/comment/approve/"+comment_pk;
     let node = comment_text.replace('{author}', author);
     node = node.replace('{created_date}', created_date);
     node = node.replace('{text}', text);
     if (user_image){
         node = node.replace('{user_image}', user_image);
     } else {
         node = node.replace('{user_image}', DEFAULT_IMAGE);
     }
     node = node.replace('{data_url}', '/news/comment/{comment_pk}/edit/');
     node = node.replace(/{comment_pk}/g, comment_pk);

     //if (may_change){
     //    let data_child = $(node).children('.date');
     //    data_child.append(remove_comment_node);
     //    data_child.append(approve_comment_node);
     //}

     let list = document.getElementsByClassName('current-comments');
     $(node).appendTo(list);
     $(".date").on("click", ".js-update-comment", loadForm);
     $("#modal-comment").on("submit", ".js-comment-update-form", saveForm);
}

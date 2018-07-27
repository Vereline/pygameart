let comment_text = "<li class=\"list-group-item comment\">\n" +
    "                                <div class=\"row\">\n" +
    "                                    <div class=\"col-xs-3 col-xl-3\">\n" +
    "                                        <img src=\"\/static\/user-default.png\" class=\"rounded-circle img-responsive\" alt=\"\" />\n" +
    "                                    </div>\n" +
    "                                    <div class=\"col-xs-10 col-xl-9\">\n" +
    "                                        <div class=\"date\">\n" +
    "                                            <a href=\"\">Comment Title</a>\n" +
    "                                            <div class=\"mic-info\">\n" +
    "                                                By: <a href=\"#\">{author}</a> {created_date}\n" +
    "                                            </div>\n" +
    "\n" +
    "                                            <div class=\"comment-text\">{text}</div>\n" +
    "                                                    <button id=\"{comment_pk}\" type=\"button\" class=\"btn btn-primary btn-xs change edit\" title=\"Edit\">\n" +
    "                                                        Edit\n" +
    "                                                    </button>\n" +
    "                                                    <button id=\"{comment_pk}\" type=\"button\" class=\"btn btn-success btn-xs change approve\" title=\"Approved\">\n" +
    "                                                        Approve\n" +
    "                                                    </button>\n" +
    "                                                    <button id=\"{comment_pk}\" type=\"button\" class=\"btn btn-danger btn-xs change remove\" title=\"Remove\">\n" +
    "                                                        Remove\n" +
    "                                                    </button>\n" +
    "                                        </div>\n" +
    "                                    </div>\n" +
    "                                </div>\n" +
    "                            </li>";
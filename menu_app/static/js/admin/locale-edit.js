$('#formContainer').prependTo($('form.admin-form'))
const langValues = new Set();

$("div.form-group input[lang]").each(function() {
    var langValue = $(this).attr("lang");
    langValues.add(langValue)
    $(this).closest("div.form-group").attr({'lang' : langValue});
    $(this).closest("div.form-group").addClass('locale');
});
$("div.form-group textarea[lang]").each(function() {
    var langValue = $(this).attr("lang");
    langValues.add(langValue)
    $(this).closest("div.form-group").attr({'lang' : langValue});
    $(this).closest("div.form-group").addClass('locale');
});

langValues.forEach((value) => {
    $("#localeTabs").append(
        `<li class="nav-item"><a class="nav-link" href="#tab-${value}">${value}</a></li>`
    )
    $("#localeTabContent").append(
        `<div class="tab-pane fade" id="tab-${value}">

        </div>`
    )
});
$("div.locale").each(function() {
    let lang = $(this).attr("lang")
    $(`.tab-pane#tab-${lang}`).append($(this));
})
$("fieldset").appendTo($('#localeTabContent #main'))

$('#localeTabs a').on('click', function (e) {
    e.preventDefault();
    $(this).tab('show');
});
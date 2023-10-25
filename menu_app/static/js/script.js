function get_subcategories(category_id) {
    $("#subcategory-header").hide()
    $.get("/categories", {category_id : category_id}
    ).done(function(data) {
        $("#search").show()
        $(".menu-badge").removeClass("active")
        $(`.menu-badge:nth-child(${category_id})`).addClass("active")
        $("#subcategories").empty();
        data['subcategories'].forEach(subcategory => {
            $("#subcategories").append(
                `<div class="subcategory">
        <button class="sub-label" name="subcategory" onclick="get_menu_items(${subcategory['subcategory_id']}, '${subcategory['subcategory_name']}', ${category_id})" type="submit" style="background-image: url(${subcategory['photo'] ? subcategory['photo'] : ""});">
            <h2 style="position: relative;">${subcategory['subcategory_name']}</h2>
        </button>
    </div>`)
        });
    }).fail(function() {
        $("#subcategories").html("<h1>Проблемы с соединением</h1>")
    });
}

function get_menu_items(subcategory_id, subcategory_name = null, category_id = 1) {
    $.get("/menu_items", {subcategory_id : subcategory_id}
    ).done(function (data) {
        $("#search").hide()
        $("#subcategory-header").html(`<h2 onclick="get_subcategories(${category_id})"><span class="bi-arrow-left-short" style="color:var(--website-secondary-color)"></span> ${subcategory_name}</h2>`)
        $("#subcategory-header").show()
        $("#subcategories").empty()
        data['menu_items'].forEach(menu_item => {
            $("#subcategories").append(
                `<div class="menu-items" id="${menu_item['item_id']}">
                <img src="/static/img/subcategories/яичницы.jpg">
                <div class="d-flex justify-content-between align-items-center mb-1">
                    <h2 class="menu-items-title mb-0">${menu_item['item_name']}</h2>
                    <span class="menu-items-description">${menu_item['weight']} г.</span>
                </div>
                <span class="menu-items-description">${menu_item['description']}</span><br>
                <span class="menu-items-description fst-italic">Состав: ${menu_item['ingredients']}</span>
                <h3 class="menu-items-price mt-2">
                    ${menu_item['price']} р.
                </h3>
            </div>`
            )
        })
    })
}

$(document).ready(() => {
    get_subcategories(1)
})

$("#location").attr("href", `https://yandex.ru/maps/?mode=search&text=${$("#location").text()}`)
$("#phone-number").attr("href", `tel:${$("#phone-number").text()}`)
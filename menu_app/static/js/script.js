function get_subcategories(category_id) {
    var test = category_id;
    $("#subcategory-header").hide()
    $.get("/categories", {category_id : category_id}
    ).done(function(data) {
        $(".menu-badge").removeClass("active")
        $(`.menu-badge:nth-child(${category_id})`).addClass("active")
        if (data['has_subcategories'] == false) {
            get_menu_items(null, null, category_id);
            return;
        }
        $("#search").show()
        $("#content").empty();
        data['subcategories'].forEach(subcategory => {
            $("#content").append(
                `<div class="subcategory">
                <button class="sub-label" name="subcategory" onclick="get_menu_items(${subcategory['subcategory_id']}, '${subcategory['subcategory_name']}')" type="submit" style="background-image: url(${subcategory['subcategory_photo'] ? subcategory['subcategory_photo'] : ""});">
                <h2 style="position: relative;">${subcategory['subcategory_name']}</h2>
                </button>
                </div>`)
            });
        }).fail(function() {
            $("#content").html("<h1>Проблемы с соединением</h1>")
        });
    }
    
    function get_menu_items(subcategory_id = null, subcategory_name = null, category_id = null) {
        $.get("/menu_items", {subcategory_id : subcategory_id, category_id : category_id}
        ).done(function (data) {
            if (category_id == null) {
                $("#search").hide()
                $("#subcategory-header").html(`<h2 onclick="get_subcategories(${data['parent_category_id']})"><span class="bi-arrow-left-short" style="color:var(--website-secondary-color)"></span> ${subcategory_name}</h2>`)
                $("#subcategory-header").show()
            }
            else {
                $("#search").show()
            }
            $("#content").empty()
            if (data['menu_items'].length == 0) {
                emptyResponseFallback()
            }
            data['menu_items'].forEach(menu_item => {
                $("#content").append(
                    `<div class="menu-items" id="${menu_item['item_id']}">
                    <img src="${menu_item['item_photo']}">
                    <div class="d-flex justify-content-between align-items-center mb-1">
                    <h2 class="menu-items-title mb-0">${menu_item['item_name']}</h2>
                    <span class="menu-items-weight">${menu_item['weight']} г.</span>
                    </div>
                    <div class="menu-items-description" onclick="expandCropText(${menu_item['item_id']});"><p>${menu_item['description']}</p></div>
                    <span class="menu-items-ingredients fst-italic">Состав: ${menu_item['ingredients']}</span>
                    <h3 class="menu-items-price mt-2">
                    ${menu_item['price']} р.
                    </h3>
                    </div>`
                    )
                    expandCropText(menu_item['item_id']);
                    bindImageClick();
                })
            }).fail(function() {
                emptyResponseFallback();
            });
        }
        
        $(document).ready(() => {
            get_subcategories(1);            
        })
        
        
        function expandCropText(item_id) {
            var description = $(`.menu-items#${item_id} .menu-items-description`);
            var text = $(`.menu-items#${item_id} .menu-items-description p`);
            
            if (description.hasClass("_has-big-description")) {
                description.removeClass("_has-big-description");
                text.removeClass("description-crop");
                return;
            }
            
            if (text.text().length > 200) {
                text.addClass("description-crop");
                description.addClass("_has-big-description");
            }
        }

        function emptyResponseFallback(param) {
            $("#content").html(`<h5 class='text-center text-white mt-5'>На данный момент тут пусто :(</h5>
                <a class='text-center' href='/'>Вернуться на главную</a>`)
        }
        
        $("#location").attr("href", `https://yandex.ru/maps/?mode=search&text=${$("#location").text()}`);
        $("#phone-number").attr("href", `tel:${$("#phone-number").text()}`);
        
        
        function openFullscreenImage(image) {
            var fullscreenImage = document.getElementById("fullscreenImage");
            var fullscreenImageSrc = document.getElementById("fullscreenImageSrc");
        
            fullscreenImageSrc.src = image.src;
            fullscreenImage.style.display = "block";
        
            setTimeout(function() {
                fullscreenImage.classList.add("show");
                fullscreenImageSrc.classList.add("show");
            }, 10);
        }
        
        function closeFullscreenImage() {
            var fullscreenImage = document.getElementById("fullscreenImage");
            var fullscreenImageSrc = document.getElementById("fullscreenImageSrc");
        
            fullscreenImage.classList.remove("show");
            fullscreenImageSrc.classList.remove("show");
        
            setTimeout(function() {
                fullscreenImage.style.display = "none";
            }, 300);
        }
        
        // Добавьте обработчики событий для открытия фотографии на полный экран
        function bindImageClick() {
            var images = document.querySelectorAll(".menu-items img");
            
            images.forEach(function(image) {
                image.addEventListener("click", function() {
                    openFullscreenImage(this);
                });
            });
        }
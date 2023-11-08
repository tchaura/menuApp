function get_subcategories(category_id) {
    $("#subcategory-header").hide();
    $.get("/categories", { category_id : category_id }).done(function (data) {
        $(".menu-badge").removeClass("active");
        $(`.menu-badge#${category_id}`).addClass("active")
        if (data['has_subcategories'] == false) {
            get_menu_items(null, null, category_id);
            return;
        }
        $("#search").show();
        $("#content").empty();
        if (data['subcategories'].length == 0) {
            emptyResponseFallback();
        }
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
        $.get("/menu_items", { subcategory_id : subcategory_id, category_id : category_id }
        ).done((data) => displayMenuItems(data, category_id ? true : false, subcategory_name)).fail(function() {
            emptyResponseFallback();
        });
    }
    
    function searchData() {
        var query = document.getElementById('search-input').value;
        $.get('/search', {query: query}).done((data) => displayMenuItems(data, true)).fail(emptyResponseFallback())
    }
    
    function displayMenuItems(data, fromSearch = false, subcategory_name = null,) {
        if (fromSearch == false) {
            $("#search").hide();
            $("#subcategory-header").html(`<h2 class="d-flex flex-row gap-2 align-items-center" onclick="get_subcategories(${data['parent_category_id']})"><span class="bi-arrow-left-short fs-1" style="color:var(--website-secondary-color)"></span> ${subcategory_name}</h2>`);
            $("#subcategory-header").show();
        }
        else {
            $("#search").show();
        }
        $("#content").empty();
        if (data['menu_items'].length == 0) {
            emptyResponseFallback();
        }
        data['menu_items'].forEach(menu_item => {
            $("#content").append(
                `<div class="menu-items" id="${menu_item['item_id']}">
                <img src="${menu_item['item_photo']}">
                <div class="d-flex justify-content-between align-items-center mb-1 flex-wrap">
                <h2 class="menu-items-title mb-0">${menu_item['item_name']}</h2>
                <span class="menu-items-weight">${menu_item['weight']} ${getCookie('lang') == 'ru' ? 'г.' : 'g.'}</span>
                </div>
                <div class="menu-items-description" onclick="expandCropText(${menu_item['item_id']});"><p>${menu_item['description']}</p></div>
                <span class="menu-items-ingredients fst-italic">Состав: ${menu_item['ingredients']}</span>
                <h3 class="menu-items-price mt-2">
                ${menu_item['price']} ${getCookie('lang') == 'ru' ? 'р.' : 'Br'}
                </h3>
                </div>`
                )
                expandCropText(menu_item['item_id']);
                bindImageClick();
            })
        }
        
        $(document).ready(() => {
            $.get('/get_first_category_id').done(function (data) {
                get_subcategories(data['category_id']);            
            });
            setCurrentLang();
            
            let searchField = $('#search .search-field')[0]
            switch (getCookie('lang')) {
                case 'en': searchField.placeholder = 'Enter search query...';
                break;
                case 'tr': searchField.placeholder = 'Arama teriminizi girin...';
                break;
                case 'zh': searchField.placeholder = '输入您的搜索词';
                break;
            }
        });
        
        
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
        
        function setCurrentLang() {
            var selector = document.querySelectorAll("#lang-select select")[0];
            var currentLang = getCookie('lang');
            selector.value = currentLang != null ? currentLang : 'ru';
        }
        
        function handleLangChange() {
            var selector = document.querySelectorAll("#lang-select select")[0];
            var lang = selector.options[selector.selectedIndex].value;
            document.cookie = `lang=${lang}; path=/; max-age=3600`;
            
            location.reload();
        }
        
        function getCookie(name) {
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2) return parts.pop().split(';').shift();
        }
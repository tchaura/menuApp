let content = $("#content");

async function get_subcategories(category_id) {
    $("#subcategory-header").hide();
    $(".menu-badge").removeClass("active");
    $(`.menu-badge#${category_id}`).addClass("active");
    await $.get("/categories", {category_id: category_id}).done(function (data) {
        content.empty();
        // slows down loading of menu items
        // TODO: remove double server request
        if (data['has_subcategories'] === false) {
            transitionTo(get_menu_items, null, null, category_id);
            return;
        }
        $("#search").show();
        content.addClass("row-cols-md-2");
        if (data['subcategories'].length === 0) {
            responseFallback(getLocaleString(LOCALE_DICTS.EMPTY_RESPONSE));
        }
        data['subcategories'].forEach(subcategory => {
            content.append(
                `<div class="subcategory col">
                        <button class="sub-label" name="subcategory" onclick="transitionTo(get_menu_items, ${subcategory['subcategory_id']}, '${subcategory['subcategory_name']}')" type="submit" style="background-color: #484848; background-image: url(${subcategory['subcategory_photo'] ? subcategory['subcategory_photo'] : ""});">
                        <h2 style="position: relative;">${subcategory['subcategory_name']}</h2>
                        </button>
                        </div>`);
        });
    }).fail(function () {
        responseFallback(getLocaleString(LOCALE_DICTS.NETWORK_ERROR))
    });
}

async function get_menu_items(subcategory_id = null, subcategory_name = null, category_id = null) {
    await $.get("/menu_items", {subcategory_id: subcategory_id, category_id: category_id}
    ).done((data) => displayMenuItems(data, !!category_id, subcategory_name)).fail(function () {
        responseFallback(getLocaleString(LOCALE_DICTS.NETWORK_ERROR));
    });
}

function displayMenuItems(data, fromSearch = false, subcategory_name = null,) {
    let areAllWithoutPhoto = data['menu_items'].every(menu_item => menu_item['item_photo'] == null);
    let subcategoryHeader = $("#subcategory-header");
    let contentWrapper = $("#content-wrapper");
    if (fromSearch === false) {
        $("#search").hide();
        subcategoryHeader.html(
            `<h2 class="d-flex flex-row gap-2 align-items-center" onclick="transitionTo(get_subcategories, ${data['parent_category_id']})"><span class="bi-arrow-left-short fs-1" style="color:var(--website-secondary-color)"></span> ${subcategory_name}</h2>`);
        subcategoryHeader.show();
    } else {
        $("#search").show();
    }
    content.empty();

    if (data['menu_items'].length === 0) {
        responseFallback(getLocaleString(LOCALE_DICTS.EMPTY_RESPONSE));
    }
    data['menu_items'].forEach(menu_item => {
        content.append(
            `<div class="menu-items col" id="${menu_item['item_id']}">
                            ${menu_item['item_photo'] ? `<img class="menu-items-img" loading="lazy" src="${menu_item['item_photo']}" alt="Menu Item"/>`: (areAllWithoutPhoto ? '' : `<div class="menu-items-img"></div>`)}
                            <div class="menu-items-header d-flex justify-content-between align-items-center mb-1">
                            <h2 class="menu-items-title mb-0">${menu_item['item_name']}</h2>
                            ${menu_item['weight'] ? `<div class="dots"></div> <span class="menu-items-weight">${menu_item['weight']} ${getLocaleString(menu_item['measure_unit'] === 'g' ? LOCALE_DICTS.MEASURE_UNIT_G : LOCALE_DICTS.MEASURE_UNIT_ML)}</span>` : ""}
                            </div>
                            ${menu_item['description'] ? `<div class="menu-items-description" onclick="expandCropText(${menu_item['item_id']});"><p>${menu_item['description']}</p></div>` : ""}
                            ${menu_item['ingredients'] ? `<span class="menu-items-ingredients fst-italic">Состав: ${menu_item['ingredients']}</span>` : ""}
                            <div class="my-2"></div>
                            <h3 class="menu-items-price">
                            ${menu_item['price']} ${getCookie('lang') === 'ru' ? 'р.' : 'Br'}
                            </h3>
                            </div>`
        )
        expandCropText(menu_item['item_id']);
        bindImageClick();
    });

    let dots = $(".dots");

    if (areAllWithoutPhoto) {
        dots.addClass("d-block");
        content.removeClass("row-cols-md-2");
        contentWrapper.addClass("without-photo");
        subcategoryHeader.addClass("without-photo");

    }
    else {
        dots.addClass("d-none");
        content.addClass("row-cols-md-2");
    }
}

function searchData() {
    const query = document.getElementById('search-input').value;
    $.get('/search', {query: query}).done((data) => displayMenuItems(data, true)).fail(() => responseFallback(getLocaleString(LOCALE_DICTS.NETWORK_ERROR)))
}

const btn = $('#scroll-top');
$(document).ready(() => {
    let firstMenuBadge = $(".menu-badge:first-child");
    if (firstMenuBadge) {
        firstMenuBadge.click();
    } else {
        responseFallback(getLocaleString(LOCALE_DICTS.EMPTY_RESPONSE));
    }
    setCurrentLang();

    if (getCookie('lang') == null) {
        document.cookie = `lang=ru; path=/; max-age=3600`;
    }


    btn.on('click', function (e) {
        e.preventDefault();
        $('html, body').animate({scrollTop: 0}, 100);
    });

    let searchField = $('#search .search-field')[0];
    searchField.placeholder = getLocaleString(LOCALE_DICTS.SEARCH_PLACEHOLDER);
});


function expandCropText(item_id) {
    const description = $(`.menu-items#${item_id} .menu-items-description`);
    const text = $(`.menu-items#${item_id} .menu-items-description p`);

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

function responseFallback(text) {
    content.removeClass("row-cols-md-2")
    content.html(
        `<div class="mt-5" style="text-align: center; color: var(--text-color)">
                            <img class="mb-3" height="70px" src="static/img/util/food-tray.png" style="opacity:0.7">
                            <h5 class='text-center'>${text}</h5>
                            <a class='text-center' style="color: var(--text-color)" href='/'>${getLocaleString(LOCALE_DICTS.RETURN_TO_MAIN)}</a>
                            </div>`
    );
}

$("#location").attr("href", `https://yandex.ru/maps/?mode=search&text=${$("#location").text()}`);
$("#phone-number").attr("href", `tel:${$("#phone-number").text()}`);


function openFullscreenImage(image) {
    var fullscreenImage = document.getElementById("fullscreenImage");
    var fullscreenImageSrc = document.getElementById("fullscreenImageSrc");

    fullscreenImageSrc.src = image.src;
    fullscreenImage.style.display = "block";

    setTimeout(function () {
        fullscreenImage.classList.add("show");
        fullscreenImageSrc.classList.add("show");
    }, 10);
}

function closeFullscreenImage() {
    let fullscreenImage = document.getElementById("fullscreenImage");
    let fullscreenImageSrc = document.getElementById("fullscreenImageSrc");

    fullscreenImage.classList.remove("show");
    fullscreenImageSrc.classList.remove("show");

    setTimeout(function () {
        fullscreenImage.style.display = "none";
    }, 300);
}

function bindImageClick() {
    let images = document.querySelectorAll(".menu-items img");

    images.forEach(function (image) {
        image.addEventListener("click", function () {
            openFullscreenImage(this);
        });
    });
}

function setCurrentLang() {
    let selector = document.querySelector("#lang-select select");
    let currentLang = getCookie('lang');
    selector.value = currentLang != null ? currentLang : 'ru';
}

function handleLangChange() {
    let selector = document.querySelectorAll("#lang-select select")[0];
    let lang = selector.options[selector.selectedIndex].value;
    document.cookie = `lang=${lang}; path=/; max-age=3600`;

    location.reload();
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

$(window).scroll(() => {
    if (window.scrollY > 300) {
        btn.fadeIn(200);
    } else {
        btn.fadeOut(200)
    }
});

function transitionTo(func, ...args) {
    let subcategoryHeader = $("#subcategory-header");
    let contentWrapper = $("#content-wrapper");
    window.scrollTo({top: 0, left: 0});
    content.fadeOut(200, () => {
        content.empty();
        loadingSpinnerShow();
        contentWrapper.removeClass("without-photo");
        subcategoryHeader.removeClass("without-photo");
        content.fadeIn(200, () => {
            func(...args).then(() => {
                content.fadeOut(0)
                content.fadeIn(200)
            })
        });
    });
}

function getLocaleString(localeDict) {
    let currentLocale = getCookie("lang");
    return localeDict[currentLocale && currentLocale in localeDict ? currentLocale : "default"];
}

const LOCALE_DICTS = {
    EMPTY_RESPONSE: {
        "default": "Похоже, тут пусто",
        "ru": "Похоже, тут пусто",
        "en": "Looks like there's nothing here",
        "tr": "Boş gibi görünüyor",
        "zh": "看起来是空的",
    },
    NETWORK_ERROR: {
        "default": "Проблемы с соединением",
        "ru": "Проблемы с соединением",
        "en": "Connection error",
        "tr": "Bağlantı sorunları",
        "zh": "连接问题",
    },
    RETURN_TO_MAIN: {
        "default": "Вернуться на главную",
        "ru": "Вернуться на главную",
        "en": "Back to main page",
        "tr": "Ana Sayfaya Geri Dön",
        "zh": "返回首页",
    },
    SEARCH_PLACEHOLDER: {
        "default": "Введите запрос для поиска...",
        "ru": "Введите запрос для поиска...",
        "en": "Enter search query...",
        "tr": "Arama teriminizi girin...",
        "zh": "输入您的搜索词",
    },
    MEASURE_UNIT_G: {
        "default": "g.",
        "ru": "г.",
    },
    MEASURE_UNIT_ML: {
        "default": "ml.",
        "ru": "мл.",
    }
}

function loadingSpinnerShow() {
    content.prepend(
        `<div class="loadingio-spinner-rolling-sk0x4g1jti"><div class="ldio-0oeqvw1sd7zb">
                    <div></div>
                    </div></div>`
    );
}

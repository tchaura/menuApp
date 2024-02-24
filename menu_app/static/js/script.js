let content = $("#content");

function displayData(category_id, has_subcategories) {
    $(".menu-badge").removeClass("active");
    $(`.menu-badge#${category_id}`).addClass("active");
    if (Boolean(has_subcategories)){
        transitionTo(get_subcategories, category_id);
    }
    else {
        transitionTo(get_menu_items, null, null, category_id);
    }
}

async function get_subcategories(category_id) {
    $("#subcategory-header").hide();
    await $.get("/categories", {category_id: category_id}).done(function (data) {
        content.empty();
        $("#search").show();
        content.addClass("row-cols-md-2");
        if (data['subcategories'].length === 0) {
            responseFallback(getLocaleString(LOCALE_DICTS.EMPTY_RESPONSE));
        }
        data['subcategories'].forEach(subcategory => {
            content.append(
                `<div class="subcategory col">
                        <div class="subcategory-wrapper">
                        <button class="sub-label" name="subcategory" onclick="transitionTo(get_menu_items, ${subcategory['subcategory_id']}, '${subcategory['subcategory_name']}')" type="submit" style="background-color: #484848; background-image: url(${subcategory['subcategory_photo'] ? subcategory['subcategory_photo'] : ""});">
                        <h2 style="position: relative;">${subcategory['subcategory_name']}</h2>
                        </button>
                        </div>
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
    let areAllWithoutPhoto = data['menu_items'].length ? data['menu_items'].every(menu_item => menu_item['item_photo'] == null || menu_item['item_photo'] === "") : false;
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
        return;
    }
    data['menu_items'].forEach(menu_item => {
        content.append(
            `<div class="menu-items col" id="${menu_item['item_id']}">
             ${menu_item['item_photo'] ? `<div class="menu-items-img-wrapper"><img class="menu-items-img" loading="lazy" src="${menu_item['item_photo']}" alt="Menu Item"/></div>`: (areAllWithoutPhoto ? '' : `<div class="menu-items-img-wrapper"><div class="menu-items-img"></div></div>`)}
             <div class="menu-items-header d-flex justify-content-between align-items-center mb-1">
             <h2 class="menu-items-title mb-0">${menu_item['item_name']}</h2>
             ${menu_item['weight'] ? `<div class="dots"></div> <span class="menu-items-weight">${menu_item['weight']} ${getLocaleString(menu_item['measure_unit'] === 'g' ? LOCALE_DICTS.MEASURE_UNIT_G : LOCALE_DICTS.MEASURE_UNIT_ML)}</span>` : ""}
             </div>
             ${menu_item['description'] ? `<div class="menu-items-description" onclick="expandCropText(${menu_item['item_id']});"><p>${menu_item['description']}</p></div>` : ""}
             ${menu_item['ingredients'] ? `<span class="menu-items-ingredients fst-italic">${ getLocaleString(LOCALE_DICTS.INGREDIENTS) + ": " + menu_item['ingredients']}</span>` : ""}
             <div class="my-2"></div>
             <h3 class="menu-items-price">
             ${menu_item['price']} ${getLocaleString(LOCALE_DICTS.CURRENCY)}
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
    let langCookie = getCookie('lang');
    let currentLang = langCookie == null ? "en" : langCookie;
    selector.value = currentLang != null ? currentLang : 'en';

    document.cookie = `lang=${currentLang}; path=/; max-age=3600`;
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
        "default": "Looks like there's nothing here",
        "ru": "Похоже, тут пусто",
        "tr": "Boş gibi görünüyor",
        "ge": "ეს ნიშნავს, რომ აქ არაფერია",
        "he": "נראה שאין כאן כלום",
    },
    NETWORK_ERROR: {
        "default": "Connection error",
        "ru": "Проблемы с соединением",
        "tr": "Bağlantı sorunları",
        "ge": "კავშირის შეფერხება",
        "he": "שגיאת חיבור",
    },
    RETURN_TO_MAIN: {
        "default": "Back to main page",
        "ru": "Вернуться на главную",
        "tr": "Ana Sayfaya Geri Dön",
        "ge": "უკან დაბრუნება მთავარ გვერდზე",
        "he": "חזור לעמוד הראשי",
    },
    SEARCH_PLACEHOLDER: {
        "default": "Search...",
        "ru": "Поиск...",
        "tr": "Arama teriminizi girin...",
        "ge": "ძიება...",
        "he": "חיפוש...",
    },
    MEASURE_UNIT_G: {
        "default": "g",
        "ru": "г",
    },
    MEASURE_UNIT_ML: {
        "default": "ml",
        "ru": "мл",
    },
    CURRENCY: {
        "default": '₾'
    },
    INGREDIENTS: {
        "default": "Ingredients",
        "ru": "Состав",
        "ge": "Συστατικά",
        "tr": "İçindekiler",
        "he": "רכיבים"
    }
};


function loadingSpinnerShow() {
    content.prepend(
        `<div class="loadingio-spinner-rolling-sk0x4g1jti"><div class="ldio-0oeqvw1sd7zb">
                    <div></div>
                    </div></div>`
    );
}

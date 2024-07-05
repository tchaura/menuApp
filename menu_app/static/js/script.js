let content = $('#content');
let lastState = {};
const btn = document.querySelector("#scroll-top");
const body = document.body;


function setScrollTop() {
    btn.addEventListener('click', function (e) {
        e.preventDefault();
        window.scrollTo({top: 0, behavior: 'smooth'});
    });

    window.addEventListener('scroll',() => {
        if (window.scrollY > 300) {
            btn.classList.add('show');
        } else {
            btn.classList.remove('show');
        }
    });
}
setScrollTop();


function setPopupFunctionality() {
    const popup = document.querySelector('#popup');

    if (!popup) return;

    const popup_button = document.querySelector('#popup-button-close');
    const close_timeout = Number(popup_button.getAttribute('delay'));
    const is_background_clickable = popup.classList.contains('close-on-click');
    const show_popup_button = document.querySelector("#show-popup");

    setTimeout(showPopup, 1000);
    setTimeout(enableCloseAbility, close_timeout * 1000);
    popup_button.addEventListener('click', hidePopup);
    show_popup_button.addEventListener('click', showPopup);

    function enableCloseAbility() {
        popup_button.style.visibility = 'visible';
        popup_button.classList.add('show');
        is_background_clickable && popup.addEventListener('click', hidePopup);
    }
    function showPopup() {
        popup.classList.remove('hide');
        show_popup_button.classList.remove('show');

        popup.classList.add('show');
        body.classList.add('no-scroll');
    }
    function hidePopup () {
        body.classList.remove('no-scroll');
        popup.classList.remove('show');

        popup.classList.add('hide');
        show_popup_button.classList.add('show');
        document.cookie = `popup_is_shown=1; path=/; max-age=36000`;

    }
}
setPopupFunctionality();

function handleCategoryClick(category_id, has_subcategories) {
    lastState.category_id = category_id;

    $(".menu-badge").removeClass("active");
    $(`#category-${category_id}`).addClass("active");
    if (Boolean(has_subcategories)){
        transitionTo(get_subcategories, category_id);
    }
    else {
        transitionTo(get_menu_items, null, category_id);
    }
}

async function get_subcategories(category_id) {
    $("#subcategory-header-wrapper").hide();
    content.empty();
    await $.get("/categories", {category_id: category_id}).done(function (data) {
        $("#search").show();
        content.addClass("row-cols-md-2");
        if (data['subcategories'].length === 0) {
            responseFallback(getLocaleString(LOCALE_DICTS.EMPTY_RESPONSE));
        }
        data['subcategories'].forEach(subcategory => {
            content.append(
                `<div class="subcategory col" onclick="transitionTo(get_menu_items, ${subcategory['subcategory_id']})">
                        <div class="subcategory-wrapper">
                        <img alt="" loading="lazy" class="subcategory-photo" src="${subcategory['subcategory_photo']}" onerror="this.src = 'static/img/util/food-tray.png'; this.classList.add('fallback')" />
                        </div>
                        <span class="subcategory-header">${subcategory['subcategory_name']}</span>
                        </div>`);
        });
    }).fail(function () {
        responseFallback(getLocaleString(LOCALE_DICTS.NETWORK_ERROR))
    });
}

async function get_menu_items(subcategory_id = null, category_id = null) {
    await $.get("/menu_items", {subcategory_id: subcategory_id, category_id: category_id}
    ).done((data) => displayMenuItems(data, !!category_id)).fail(function () {
        responseFallback(getLocaleString(LOCALE_DICTS.NETWORK_ERROR));
    });
}

function displayMenuItems(data, fromSearch = false) {
    let areAllWithoutPhoto = data['menu_items'].length ? data['menu_items'].every(menu_item => menu_item['item_photo'] == null || menu_item['item_photo'] === "") : false;
    let subcategoryHeaderWrapper = $("#subcategory-header-wrapper");
    let contentWrapper = $("#content-wrapper");
    if (fromSearch) {
        $("#search").show();
    } else {
        $("#search").hide();
        subcategoryHeaderWrapper.html(
            `<h2 id="subcategory-header" class="d-flex flex-row gap-2 align-items-center" onclick="transitionTo(get_subcategories, ${data['parent_category_id']})"><span class="bi-arrow-left-short fs-1" style="color:var(--website-secondary-color)"></span> ${data['parent_subcategory_name']}</h2>`);
        subcategoryHeaderWrapper.show();
    }
    content.empty();

    if (data['menu_items'].length === 0) {
        responseFallback(getLocaleString(LOCALE_DICTS.EMPTY_RESPONSE));
        return;
    }
    data['menu_items'].forEach(menu_item => {
        content.append(
            `<div class="menu-items col" id="${menu_item['item_id']}">
             ${menu_item['item_photo'] ? `<div class="menu-items-img-wrapper"><img class="menu-items-img" loading="lazy" onerror="this.src = 'static/img/util/food-tray.png'; this.classList.add('fallback')" src="${menu_item['item_photo']}" alt="Menu Item"/></div>`: (areAllWithoutPhoto ? '' : `<div class="menu-items-img-wrapper"><div class="menu-items-img"></div></div>`)}
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
        subcategoryHeaderWrapper.addClass("without-photo");

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

$(document).ready(() => {
    let firstMenuBadge = $(".menu-badge:first-child");
    if (firstMenuBadge) {
        firstMenuBadge.click()
        lastState = {
            'func': () => {firstMenuBadge.click()}
        }
    } else {
        responseFallback(getLocaleString(LOCALE_DICTS.EMPTY_RESPONSE));
    }

    setDefaults();
});

function setDefaults() {
    setCurrentLang();
    let location = $("#location");
    location.attr("href", `https://maps.app.goo.gl/awA2hp3PjfrwyD2i7`);
    let phoneNumber = $("#phone-number");
    phoneNumber.attr("href", `tel:${phoneNumber.text()}`);
    let searchField = $('#search .search-field')[0];
    searchField.placeholder = getLocaleString(LOCALE_DICTS.SEARCH_PLACEHOLDER);
}


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

    if (currentLang === 'fa' || currentLang === 'ar') {
        document.querySelector("html").setAttribute("dir", "rtl");
    }
    else {
        document.querySelector("html").setAttribute("dir", "ltr")
    }
    selector.value = currentLang != null ? currentLang : 'en';

    document.cookie = `lang=${currentLang}; path=/; max-age=3600`;
}

async function handleLangChange() {
    let selector = document.querySelectorAll("#lang-select select")[0];
    let lang = selector.options[selector.selectedIndex].value;
    document.cookie = `lang=${lang}; path=/; max-age=3600`;
    lastState.scrollY = window.scrollY;
    let dp = new DOMParser();
    await $.get("/").done(async (data) => {
        document.querySelector("body").innerHTML = dp.parseFromString(data, 'text/html').querySelector("body").innerHTML;
        setDefaults();
        content = $("#content");
        lastState.func();
        document.querySelector(`#category-${lastState.category_id}`).classList.add('active')
    })
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function transitionTo(func, ...args) {
    lastState.func =  () => transitionTo(func, ...args);

    let subcategoryHeaderWrapper = $("#subcategory-header-wrapper");
    let contentWrapper = $("#content-wrapper");
    let footer = $("footer");
    content.fadeOut(200, () => {
        footer.hide();
        subcategoryHeaderWrapper.hide(100);
        content.empty();
        loadingSpinnerShow();
        contentWrapper.removeClass("without-photo");
        subcategoryHeaderWrapper.removeClass("without-photo");
        content.fadeIn(200, () => {
            func(...args).then(() => {
                content.fadeOut(0)
                footer.show();
                content.fadeIn(200)
            })
        });
    });
}

function getLocaleString(localeDict) {
    let currentLocale = getCookie("lang");
    return localeDict[currentLocale && currentLocale in localeDict ? currentLocale : "default"];
}

function loadingSpinnerShow() {
    content.prepend(
        `<div class="loadingio-spinner-rolling-sk0x4g1jti"><div class="ldio-0oeqvw1sd7zb">
                    <div></div>
                    </div></div>`
    );
}

const LOCALE_DICTS = {
    EMPTY_RESPONSE: {
        "default": "Looks like there's nothing here",
        "ru": "Похоже, тут пусто",
        "tr": "Boş gibi görünüyor",
        "ge": "ეს ნიშნავს, რომ აქ არაფერია",
        "ar": "يبدو أنه لا يوجد شيء هنا",
        "fa": "به نظر می رسد اینجا چیزی نیست",
    },
    NETWORK_ERROR: {
        "default": "Connection error",
        "ru": "Проблемы с соединением",
        "tr": "Bağlantı sorunları",
        "ge": "კავშირის შეფერხება",
        "ar": "خطأ في الاتصال",
        "fa": "خطای اتصال",
    },
    RETURN_TO_MAIN: {
        "default": "Back to main page",
        "ru": "Вернуться на главную",
        "tr": "Ana Sayfaya Geri Dön",
        "ge": "უკან დაბრუნება მთავარ გვერდზე",
        "ar": "العودة إلى الصفحة الرئيسية",
        "fa": "بازگشت به صفحه اصلی",
    },
    SEARCH_PLACEHOLDER: {
        "default": "Search...",
        "ru": "Поиск...",
        "tr": "Arama teriminizi girin...",
        "ge": "ძიება...",
        "ar": "بحث...",
        "fa": "جستجو...",
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
        "ar": "المكونات",
        "fa": "المكونات",
    }
};
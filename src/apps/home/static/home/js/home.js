// static/home/js/home.js
document.addEventListener('DOMContentLoaded', function () {
    // منوی کشویی
    const dropbtn = document.querySelector('.dropbtn');
    const dropdownContent = document.querySelector('.dropdown-content');

    if (dropbtn && dropdownContent) {
        dropbtn.addEventListener('click', function () {
            dropdownContent.style.display =
                dropdownContent.style.display === 'block' ? 'none' : 'block';
        });

        document.addEventListener('click', function (event) {
            if (!dropbtn.contains(event.target) && !dropdownContent.contains(event.target)) {
                dropdownContent.style.display = 'none';
            }
        });
    }

    // اسلایدر پرفروش‌ترین
    new Swiper('.top-selling-swiper', {
        slidesPerView: 'auto',
        spaceBetween: 10, // فاصله کمتر برای جا دادن 5 اسلاید
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        breakpoints: {
            900: {
                slidesPerView: 5, // 5 اسلاید تو دسکتاپ
            },
            600: {
                slidesPerView: 3, // 3 اسلاید تو تبلت
            },
            0: {
                slidesPerView: 2, // 2 اسلاید تو موبایل
            },
        },
    });

    // اسلایدر پربازدیدترین
    new Swiper('.most-viewed-swiper', {
        slidesPerView: 'auto',
        spaceBetween: 10, // فاصله کمتر
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        breakpoints: {
            900: {
                slidesPerView: 5, // 5 اسلاید تو دسکتاپ
            },
            600: {
                slidesPerView: 3, // 3 اسلاید تو تبلت
            },
            0: {
                slidesPerView: 2, // 2 اسلاید تو موبایل
            },
        },
    });
});
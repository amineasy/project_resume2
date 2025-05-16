document.addEventListener('DOMContentLoaded', function () {
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

    // مدیریت زیرمنوها
    const dropdownItems = document.querySelectorAll('.dropdown-item');
    dropdownItems.forEach(item => {
        const subcontent = item.querySelector('.dropdown-subcontent');
        if (subcontent) {
            item.addEventListener('mouseenter', () => {
                subcontent.style.display = 'block';
            });
            item.addEventListener('mouseleave', () => {
                subcontent.style.display = 'none';
            });
        }
    });
});
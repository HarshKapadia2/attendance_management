(
    () =>
    {
        const burger = document.querySelector('.burger');
        const nav = document.querySelector('.navbar-elements');

        burger.addEventListener
        (
            'click',
            () =>
            {
                //toggle burger menu
                nav.classList.toggle('burger-active');

                // burger animation
                burger.classList.toggle('toggle');
            }
        )
    }
)();
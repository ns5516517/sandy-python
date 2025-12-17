function match_height() {
    $('.match_height_col').matchHeight();
    $('.match_height_txt').matchHeight();
}
match_height();

if ($('.collection_slider').length) {
    $('.collection_slider').owlCarousel({
        loop: true,
        // autoplay: true,
        // autoplayTimeout: 4000,
        // autoplaySpeed: 2000,
        margin: 0,
        nav: false,
        dots: true,
        navText: ["<i class='far fa-angle-left'></i>", "<i class='far fa-angle-right'></i>"],
        responsive: {
            0: {
                items: 1
            },
            567: {
                items: 1
            },
            768: {
                items: 1
            },
        }
    });
}


$('body').on('click', '.menu_btn', function () {
    var headerHeight = $(this).closest('.header_section').outerHeight();

    if ($('.open_menu').hasClass('show')) {
        $('.open_menu').removeClass('show').css('margin-top', '');
        $('body').removeClass('scroll_off');
        $(this).find(".far").removeClass('fa-times').addClass('fa-bars');
    } else {
        $('.open_menu').addClass('show').css('margin-top', headerHeight + 'px');
        $('body').addClass('scroll_off');
        $(this).find(".far").removeClass('fa-bars').addClass('fa-times');
    }
});

if ($('.quantity_cart').length) {
    let addInCart = {
        body: null,
        plusNumber: null,
        minusNumber: null,
        data: [],
        total_price: 0,

        init: function () {
            this.body = $('body');
            this.plusNumber = '.item_cart .plus';
            this.minusNumber = '.item_cart .minus';

            this.body.on('click', this.plusNumber, this.plusNumberCounter);
            this.body.on('click', this.minusNumber, this.minusNumberCounter);

            let data_div = Array.from($('.quantity_cart').find('.item_cart'));
            let extractedData = data_div.map((item) => {
                let name = $(item).data('itemName');
                let size = $(item).data('itemSize');
                let price = $(item).data('itemPrice');
                let id = $(item).data('itemId');
                let quantity = $(item).data('itemQuantity')
                let flavour = $(item).data('flavour')
                let weight = $(item).data('weight')
                let variant_type = $(item).data('type')
                let obj = { name: name, size: size, price: price, id: id, quantity: quantity, flavour: flavour, weight: weight, variant_type: variant_type };
                return obj
            });
            this.data = extractedData;
            this.updateUi()
        },
        updateCart: function (that, num) {
            let parentItem = that.closest('.item_cart');
            let input = parentItem.find('input');
            let itemId = parentItem.data('itemId')
            let newQuantity = input.val();
            let itemIndex = this.data.findIndex((item) => item.id === itemId)
            if (itemIndex !== -1) {
                this.data[itemIndex].quantity = newQuantity
            }

            $.ajax({
                type: "post",
                url: "/update-cart/",
                data: {
                    'quantity': num,
                    'id': itemId
                },
                beforeSend: function () {
                    addInCart.updateUi();
                },
                success: function (response) {
                },
                error: function (xhr, status, error) {
                }
            });
        },

        updateUi: function () {
            let inner_bill = $('.quantity_cart').find('.inner_bill')
            let total_div = $('.quantity_cart').find('.total_price').find('.right_b')
            let btn = $('.quantity_cart').find('.btn_area')
            btn.empty()
            total_div.empty();
            inner_bill.empty();
            console.log(this.data)

            let htmlContent = this.data?.map((item) => {
                return `
                <div class="top item_variant_listing">
                <div class="left_b">
                <h6 class="item_quantity">${item.name} - ${item.variant_type == 'merchandise' ? item.size : item.flavour} x ${item.quantity}</h6>
                </div>
                <div class="right_b">
                <div class="dollar item_total_price">$ ${item.price * item.quantity}</div>
                </div>
                </div>
                `
            }).join('')
            inner_bill.append(htmlContent)

            let total = this?.data?.reduce((acc, currentVal) => acc + (Number(currentVal.price * currentVal.quantity)), 0)
            let total_html_content = `
                <div class="dollar">$${total}</div>
            `
            total_div.append(total_html_content);
            btn.append(`<a href="javascript:;" class="btn-primary">Pay AUD ${total}</a>`)
        },

        plusNumberCounter: function () {
            let that = $(this);
            let input = that.parent().find('input');
            input.val(parseInt(input.val()) + 1);
            input.change();
            addInCart.updateCart(that, 1);
            return false;
        },
        minusNumberCounter: function () {
            let that = $(this);
            let input = that.parent().find('input');
            let count = parseInt(input.val()) - 1;
            count = count < 1 ? 1 : count;
            input.val(count);
            input.change();
            addInCart.updateCart(that, -1)
            return false;
        }
    }

    addInCart.init();
}

if ($('.supplement_detail_section').length) {
    let updateUi = {
        body: $('body'),
        selected_flavoured_id: 1,
        selected_flavoured_size_id: 1,
        plusNumber: null,
        minusNumber: null,
        slug: '',

        init: function () {
            this.filterData();
            this.getSelectedId();
            this.getSelectedSizeId();
            this.plusNumber = '#number .plus';
            this.minusNumber = '#number .minus';
            this.slug = $('.supplement_detail_section').data('slug')

            this.body.on('click', this.plusNumber, this.plusNumberCounter);
            this.body.on('click', this.minusNumber, this.minusNumberCounter);
        },

        filterData: function () {
            const flavourWeightList = $('.supplement_detail_section .size_list').first().find('li');
            let pricing = Array.from($('.supplement_detail_section').find('.price_main'));
            let stock_listing = Array.from($('.supplement_detail_section').find('.stock'));

            pricing.forEach((item) => {
                let priceId = $(item).data('flavourSizeId');
                if (priceId == this.selected_flavoured_size_id) {
                    $(item).show();
                } else {
                    $(item).hide();
                }
            });

            stock_listing.forEach((item) => {
                let stockId = $(item).data('flavourSizeId');
                if (stockId == this.selected_flavoured_size_id) {
                    $(item).show();
                } else {
                    $(item).hide();
                }
            });
            flavourWeightList.each((i, item) => {
                let sizeId = $(item).data('flavourId')
                if (sizeId == this.selected_flavoured_id) {
                    $(item).show();
                }
                else {
                    $(item).hide();
                }
            });
        },

        getSelectedId: function () {
            const flavourList = $('.supplement_detail_section .flavour_main li');

            if (flavourList.length) {
                flavourList.first().addClass('active');
                this.selected_flavoured_id = flavourList.first().data('flavourId');
            }

            flavourList.on('click', (e) => {
                flavourList.removeClass('active');
                const clickedItem = $(e.currentTarget);
                clickedItem.addClass('active');
                this.selected_flavoured_id = clickedItem.data('flavourId');
                this.filterData();
                this.getSelectedSizeId();
                this.update_btn()
            });
        },

        getSelectedSizeId: function () {
            let size_list = $('.supplement_detail_section').find('.size_list')[0];
            let newArr = Array.from($(size_list).find('li'));

            if (newArr.length > 0) {
                newArr.forEach(ele => ele.classList.remove('active'));
                newArr[0].classList.add('active');
                this.selected_flavoured_size_id = $(newArr[0]).data('flavourSizeId');
            }

            let visibleSizes = $(newArr).filter(':visible');
            if (visibleSizes.length) {
                visibleSizes.removeClass('active');
                visibleSizes.first().addClass('active');
                this.selected_flavoured_size_id = visibleSizes.first().data('flavourSizeId');
            }

            newArr.forEach((item) => {
                item.addEventListener('click', (e) => {
                    newArr.forEach(ele => ele.classList.remove('active'));
                    let clickedItem = e.currentTarget;
                    clickedItem.classList.add('active');
                    this.selected_flavoured_size_id = $(clickedItem).data('flavourSizeId');
                    this.filterData();
                    this.update_btn();
                });
            });

            this.filterData();
        },

        update_btn: function () {
            let cart_btn = $('.supplement_detail_section').find('#cart_btn')
            cart_btn.find('#add_cart_btn').remove()
            let htmlContent = `
            <a href="/add/${this.selected_flavoured_size_id}" class="btn-primary" id="add_cart_btn">Add to Cart</a>`
            cart_btn.append(htmlContent)
        },

        plusNumberCounter: function () {
            let that = $(this);
            let input = that.parent().find('input');
            input.val(parseInt(input.val()) + 1);
            input.change();
            updateUi.updateCart(that, 1);
            return false;
        },

        minusNumberCounter: function () {
            let that = $(this);
            let input = that.parent().find('input');
            let count = parseInt(input.val()) - 1;
            count = count < 1 ? 1 : count;
            input.val(count);
            input.change();
            updateUi.updateCart(that, -1)
            return false;
        },

        updateCart: function (that, num) {
            let parentItem = that.closest('.inner_content');
            let input = parentItem.find('input');
            let newQuantity = input.val();

            $.ajax({
                type: "post",
                url: "/update-cart/",
                data: {
                    'quantity': num,
                    'size_id': this.selected_flavoured_size_id
                },
                beforeSend: function () {
                    // addInCart.updateUi();
                },
                success: function (response) {
                },
                error: function (xhr, status, error) {
                }
            });
        },

    };

    updateUi.init();
}










Fancybox.bind("[data-fancybox]", {
    Toolbar: {
        display: ["close"],
    },
    closeButton: "top",
});


if ($('#swiper_supplement').length) {
    var swiperSupple = new Swiper("#swiper_supplementThumb", {
        spaceBetween: 10,
        slidesPerView: 4,
        freeMode: true,
        watchSlidesProgress: true,
    });
    var swiper2 = new Swiper("#swiper_supplement", {
        spaceBetween: 10,
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
        },
        thumbs: {
            swiper: swiperSupple,
        },
    });
}

// 

let allCards = document.querySelectorAll('.card_item')
allCards.forEach((card, index) => {
    let newIndex = index + 1
    card.addEventListener('mouseenter', (e) => {
        allCards.forEach(c => c.classList.remove('active'));
        let id = Number(e.target.dataset.id)
        if (id === newIndex) {
            e.target.classList.toggle('active')
        }
    })
})

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.modal').forEach((modal) => {
        let size = modal.querySelector('.actual_size')
        let price = modal.querySelector('.price')
        let add_to_cart_id = modal.querySelector('#add_to_cart')
        modal.querySelectorAll('.size_list').forEach((parent) => {
            let list = parent.querySelectorAll('li')
            list.forEach((item) => {
                item.addEventListener('click', (e) => {
                    list.forEach((i) => i.classList.remove('active'))
                    let targetPrice = e.target.dataset.price
                    let productId = e.target.dataset.productId
                    let variantId = e.target.dataset.variantId
                    e.target.classList.toggle('active')
                    size.innerText = e.target.innerText
                    price.innerText = `$${targetPrice}`
                    if (add_to_cart_id) {
                        add_to_cart_id.href = `/add/${variantId}`
                    }
                })
            })
        })
    })
})
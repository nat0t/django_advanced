window.onload = () => {
    $('.basket-list').on('click', 'input[type="number"]', () => {
        const t_href = event.target;
        $.ajax({
            url: `/baskets/edit/${t_href.name}/${t_href.value}/`,
            success: (data) => {
                $('.basket-list').html(data.result);
            },
        });
        event.preventDefault();
    });
}
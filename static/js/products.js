window.onload = () => {
    $('.categories_list').on('click', 'a', () => {
        let link = event.target.href;

        $.ajax({
            url: link,
            success: (data) => {
                $(".ajax").html(data.result);
            },
        });

        event.preventDefault();
    });
    $('.ajax').on('click', 'a', () => {
        let link = event.target.href;

        $.ajax({
            url: link,
            success: (data) => {
                $(".ajax").html(data.result);
            },
        });

        event.preventDefault();
    });
}

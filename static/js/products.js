window.onload = () => {
    $('.categories_list').on('click', 'a', () => {
        let link = event.target.href;

        $.ajax({
            url: link,
            success: (data) => {
                // Hardcodded for now
                if (data.hasOwnProperty('result')) {
                    $(".ajax").html(data.result);
                } else {
                    let index = link.indexOf('/products')
                    let url = link.substr(0, index)
                    // window.location.replace(link.);
                    window.location.replace(`${url}${data}`);
                    // $("html").html(data);
                }
            },
        });

        event.preventDefault();
    });
    $('.ajax').on('click', '.paginator_list a', () => {
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

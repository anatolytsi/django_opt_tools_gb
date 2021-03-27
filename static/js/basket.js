window.onload = () => {
    $(".basket_list").on("click", "input[type='number']", () => {
        let tHref = event.target;

        $.ajax({
            url: `/baskets/edit/${tHref.name}/${tHref.value}/`,
            success: (data) => {
                $(".basket_list").html(data.result);
            },
        });

        event.preventDefault();
    })
}

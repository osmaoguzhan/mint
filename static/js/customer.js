const deleteCustomer = (id) => {
    let csrftoken = getCookie('csrftoken');
    Swal.fire(
        {
            title: 'Are you sure? You want to delete this customer?',
            text: "You won't be able to revert this!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Delete'
        }
    ).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: `/customers/${id}/delete`,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                success: function () {
                    Swal.fire(
                        'Deleted!',
                        'The customer has been deleted.',
                        'success'
                    ).then(() => {
                        location.reload();
                    });

                },
                error: function (data) {
                    Swal.fire(
                        'Error!',
                        'Something went wrong while deleting the customer.',
                        'error'
                    )
                }
            })

        }
    })
}

function sort(order_by) {
    let queryStr = window.location.search;
    const urlParams = new URLSearchParams(queryStr);
    for (let param of urlParams) {
        console.log(param)
    }
    let value = urlParams.get('value');
    let order = urlParams.get('order_by');
    let query = urlParams.get('query');
    if (value === 'desc' || value === null || order !== order_by) {
        value = 'asc';
    } else {
        value = 'desc';
    }
    let path = '?order_by=' + order_by + '&value=' + value;
    window.location.href = query ? path + '&query=' + query : path;
}
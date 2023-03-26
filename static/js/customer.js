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
                success: () => {
                    Swal.fire(
                        'Deleted!',
                        'The customer has been deleted.',
                        'success'
                    ).then(() => {
                        location.reload();
                    });

                },
                error: () => {
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
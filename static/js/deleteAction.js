const deleteActionMessages = {
    'en': {
        'title': `Are you sure?`,
        'text': 'You won\'t be able to revert this! All related data will be deleted as well.',
        'delete': 'Delete',
        'deleted': 'Deleted!',
        'deleted_text': `Successfully deleted.`,
        'error': 'Error!',
        'error_text': `Something went wrong while deleting.`,
        'cancel': 'Cancel'
    },
    'pl': {
        'title': 'Czy na pewno chcesz usunąć ten element?',
        'text': 'Nie będziesz mógł tego cofnąć! Wszystkie powiązane dane zostaną usunięte.',
        'delete': 'Usuń',
        'deleted': 'Usunięto!',
        'deleted_text': 'Element został usunięty.',
        'error': 'Błąd!',
        'error_text': 'Wystąpił błąd podczas usuwania elementu.',
        'cancel': 'Anuluj'
    },
    'tr': {
        'title': 'Emin misiniz?',
        'text': 'Bu işlemi geri alamazsınız! Bu işlemle ilgili tüm veriler de silinecektir.',
        'delete': 'Sil',
        'deleted': 'Silindi!',
        'deleted_text': 'Başarıyla silindi.',
        'error': 'Hata!',
        'error_text': 'Silinirken bir hata oluştu.',
        'cancel': 'İptal'
    }
}

const deleteAction = (item, id) => {
    let csrftoken = getCookie('csrftoken');
    let lang = getCookie('django_language');
    let msg = deleteActionMessages[lang];
    Swal.fire(
        {
            title: msg.title,
            text: msg.text,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            cancelButtonText: msg.cancel,
            confirmButtonText: msg.delete
        }
    ).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: `/${lang}/${item}s/${id}/delete/`,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                success: () => {
                    Swal.fire(
                        msg.deleted,
                        msg.deleted_text,
                        'success'
                    ).then(() => {
                        location.reload();
                    });

                },
                error: () => {
                    Swal.fire(
                        msg.error,
                        msg.error_text,
                        'error'
                    )
                }
            })

        }
    })
}
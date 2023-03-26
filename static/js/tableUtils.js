const exportTable = () => {
    Swal.fire({
        icon: 'info',
        text: 'You can export the table to PDF or Excel',
        showCloseButton: true,
        showCancelButton: true,
        focusConfirm: false,
        confirmButtonText:
            '<i class="fa-solid fa-file-excel"></i> Excel',
        cancelButtonText:
            '<i class="fa-solid fa-file-pdf"></i> PDF',
    }).then((result) => {
        if (result.isConfirmed) {
            htmlTableToExcel();
            window.location.reload();
        } else if (result.dismiss === Swal.DismissReason.cancel) {
            exportPDF();
            window.location.reload();
        }
    })
}
const exportPDF = () => {
    let table = document.getElementById("tableToExport");
    let oldPage = document.body.innerHTML;
    table = clean(table);
    document.body.innerHTML = table.outerHTML;
    window.print();
    document.body.innerHTML = oldPage;
}

const htmlTableToExcel = () => {
    let table = document.getElementById("tableToExport");
    let oldPage = document.body.innerHTML;
    table = clean(table);
    let excelFile = XLSX.utils.table_to_book(table, {sheet: "sheet1"});
    XLSX.write(excelFile, {bookType: 'xlsx', bookSST: true, type: 'base64'});
    XLSX.writeFile(excelFile, 'ExportedFile:HTMLTableToExcel.xlsx');
    document.body.innerHTML = oldPage;
}

const clean = (table) => {
    table.querySelectorAll("tr").forEach((row, idx) => {
        if (idx === 0) {
            row.querySelector("th:last-child").remove();
            row.querySelector("th:last-child").remove();
        } else {
            row.querySelector("td:last-child").remove();
            row.querySelector("td:last-child").remove();
        }
    });
    return table;
}

$(window).on('load', () => {
    let urlParams = new URLSearchParams(window.location.search);
    let order_by = urlParams.get('order_by');
    let value = urlParams.get('value');
    let query = urlParams.get('query');
    if (order_by !== null || value !== null || query !== null) {
        $('#clearFilters').css('display', 'inline-block');
    } else {
        $('#clearFilters').css('display', 'none');
    }
});

const sort = (order_by) => {
    let queryStr = window.location.search;
    const urlParams = new URLSearchParams(queryStr);
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
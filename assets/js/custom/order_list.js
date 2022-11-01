
// $("#edit-button").on("click", function (e) {
//     e.preventDefault();
//     let currentElement = $(this);
//     Swal.fire({
//         title: 'Do you want to edit the order?',
//         showDenyButton: true,
//         // showCancelButton: true,
//         confirmButtonText: 'Yes',
//         denyButtonText: 'No',
//         customClass: {
//           actions: 'my-actions',
//           cancelButton: 'order-1 right-gap',
//           confirmButton: 'order-2',
//           denyButton: 'order-3',
//         }
//       }).then((result) => {
//         if (result.isConfirmed) {
//             window.location.href = currentElement.attr('href');
//         } else if (result.isDenied) {
//         //   Swal.fire('Ok not editing :)', '', 'info')
//         }
//       })
// })

// $("#exchange-button").on("click", function (e) {
//     e.preventDefault();
//     let currentElement = $(this);
//     Swal.fire({
//         title: 'Do you want to exchange the order?',
//         text: 'Exchange will create a new order and mark the existing order as Exchange',
//         showDenyButton: true,
//         // showCancelButton: true,
//         confirmButtonText: 'Yes',
//         denyButtonText: 'No',
//         customClass: {
//           actions: 'my-actions',
//           cancelButton: 'order-1 right-gap',
//           confirmButton: 'order-2',
//           denyButton: 'order-3',
//         }
//       }).then((result) => {
//         if (result.isConfirmed) {
//             window.location.href = currentElement.attr('href');
//         } else if (result.isDenied) {
//           Swal.fire('Ok No Exchange Order Created', '', 'info')
//         }
//       })
// })

// "use strict";

// // Class definition
// var KTDatatablesExample = function () {
//     // Shared variables
//     var table;
//     var datatable;

//     // Private functions
//     var initDatatable = function () {
//         // Set date data order
//         const tableRows = table.querySelectorAll('tbody tr');

//         tableRows.forEach(row => {
//             const dateRow = row.querySelectorAll('td');
//             // const realDate = moment(dateRow[3].innerHTML, "DD MMM YYYY, LT").format(); // select date from 4th column in table
//             // dateRow[3].setAttribute('data-order', realDate);
//         });

//         // Init datatable --- more info on datatables: https://datatables.net/manual/
//         datatable = $(table).DataTable({
//             "info": false,
//             'order': [],
//             'pageLength': 50,
//             "lengthMenu": [ 10, 25, 50, 75, 100, 200 ]
//         });
//     }

//     // Hook export buttons
//     var exportButtons = () => {
//         const documentTitle = 'Customer Orders Report';
//         var buttons = new $.fn.dataTable.Buttons(table, {
//             buttons: [
//                 {
//                     extend: 'copyHtml5',
//                     columns: [ 1, 2, 3, 4,5,6,7,8,9,11 ]
//                 },
//                 {
//                     extend: 'excelHtml5',
//                     exportOptions: {
//                         columns: [ 1, 2, 3, 4,5,6,8,10]
//                     },
//                     title: null
//                 },
//                 {
//                     extend: 'csvHtml5',
//                     title: documentTitle
//                 },
//                 {
//                     extend: 'pdfHtml5',
//                     title: documentTitle
//                 }

                
//             ]
//         }).container().appendTo($('#kt_datatable_example_buttons'));

//         // Hook dropdown menu click event to datatable export buttons
//         const exportButtons = document.querySelectorAll('#kt_datatable_example_export_menu [data-kt-export]');
//         exportButtons.forEach(exportButton => {
//             exportButton.addEventListener('click', e => {
//                 e.preventDefault();

//                 // Get clicked export value
//                 const exportValue = e.target.getAttribute('data-kt-export');
//                 const target = document.querySelector('.dt-buttons .buttons-' + exportValue);

//                 // Trigger click event on hidden datatable export buttons
//                 target.click();
//             });
//         });
//     }

//     // Search Datatable --- official docs reference: https://datatables.net/reference/api/search()
//     var handleSearchDatatable = () => {
//         const filterSearch = document.querySelector('[data-kt-filter="search"]');
//         filterSearch.addEventListener('keyup', function (e) {
//             datatable.search(e.target.value).draw();
//         });
//     }

//     // Public methods
//     return {
//         init: function () {
//             table = document.querySelector('#kt_datatable_example');

//             if ( !table ) {
//                 return;
//             }

//             initDatatable();
//             exportButtons();
//             handleSearchDatatable();
//         }
//     };
// }();

// // On document ready
// KTUtil.onDOMContentLoaded(function () {
//     KTDatatablesExample.init();
// });


<link rel="stylesheet" type="text/css" href="../css/jquery.dataTables.min.css">
    <link rel="stylesheet" type="text/css" href="../css/buttons.dataTables.min.css">
    <style type="text/css" class="init">
    .dataTables_length {
      margin-left:200px;
    }
    </style>
	<script type="text/javascript" src="../js/jquery-3.3.1.js"></script>
	<script type="text/javascript" src="../js/jquery.dataTables.min.js"></script>
	<script type="text/javascript" src="../js/dataTables.buttons.min.js"></script>
	<script type="text/javascript" src="../js/buttons.flash.min.js"></script>
	<script type="text/javascript" src="../js/jszip.min.js"></script>
	<script type="text/javascript" src="../js/pdfmake.min.js"></script>
	<script type="text/javascript" src="../js/vfs_fonts.js"></script>
	<script type="text/javascript" src="../js/buttons.html5.min.js"></script>
    <script type="text/javascript" src="../js/buttons.print.min.js"></script>
    <script type="text/javascript" src="../js/buttons.colVis.min.js"></script>
	<script type="text/javascript" class="init">
    $(document).ready(function() {
    $('#example').DataTable( {
        dom: 'Blfrtip',
        buttons: [
            {
                extend: 'print',
                exportOptions: {
                    //columns: [ 0, ':visible' ]
                    columns: ':visible'
                }
            },
            {
                extend: 'excelHtml5',
                exportOptions: {
                    columns: ':visible'
                }
            },
            {
                extend: 'pdfHtml5',
                orientation: 'landscape',
                pageSize: 'A2',
                exportOptions: {
                    columns: ':visible'
                //columns: [ 0, 1, 2, 3, 4, 5 ]
                }
            },
            'colvis'
        ]
    } );
} );
	</script>
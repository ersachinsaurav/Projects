<script type='text/javascript'>
    function preview_emp_photo(event) {
        var reader = new FileReader();
        reader.onload = function() {
            var output = document.getElementById('emp_photo');
            output.src = reader.result;
        }
        reader.readAsDataURL(event.target.files[0]);
    }

    function preview_doc1(event) {
        var reader = new FileReader();
        reader.onload = function() {
            var output = document.getElementById('doc1');
            output.src = reader.result;
        }
        reader.readAsDataURL(event.target.files[0]);
    }
    
    function preview_doc2(event) {
        var reader = new FileReader();
        reader.onload = function() {
            var output = document.getElementById('doc2');
            output.src = reader.result;
        }
        reader.readAsDataURL(event.target.files[0]);
    }

</script>
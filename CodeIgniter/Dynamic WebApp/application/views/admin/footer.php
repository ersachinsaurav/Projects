  <!-- Main Footer -->
  <footer class="main-footer">
    <!-- To the right -->
    <div class="float-right d-none d-sm-inline">
      Last Updated: 24/02/2021
    </div>
    <!-- Default to the left -->
    <strong>Copyright &copy; 2021-2022 <a href="<?php echo base_url()?>">EnspyrME</a>.</strong> All rights reserved.
  </footer>
</div>
<!-- ./wrapper -->

<!-- REQUIRED SCRIPTS -->

<!-- jQuery -->
<script src="<?php echo base_url()?>public/admin/plugins/jquery/jquery.min.js"></script>
<!-- Text Editor -->
<script src="<?php echo base_url()?>public/admin/plugins/summernote/summernote-bs4.js"></script>
<!-- Bootstrap 4 -->
<script src="<?php echo base_url()?>public/admin/plugins/bootstrap/js/bootstrap.bundle.min.js"></script>
<!-- AdminLTE App -->
<script src="<?php echo base_url()?>public/admin/dist/js/adminlte.min.js"></script>

<!-- Editor App -->
<script>
  $(function(){
    $('textarea').summernote({
      height: '400px'
    })
  })
</script>

</body>
</html>
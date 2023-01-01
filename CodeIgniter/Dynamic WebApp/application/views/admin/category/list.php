<?php $this->load->view('admin/header');?>

  <!-- Content Wrapper. Contains page content -->
  <div class="content-wrapper">
    <!-- Content Header (Page header) -->
    <div class="content-header">
      <div class="container-fluid">
        <div class="row mb-2">
          <div class="col-sm-6">
            <h1 class="m-0 text-dark">Categories</h1>
          </div><!-- /.col -->
          </div><!-- /.row -->
      </div><!-- /.container-fluid -->
    </div>
    <!-- /.content-header -->

    <!-- Main content -->
    <div class="content">
      <div class="container-fluid">
        <div class="row">
          <div class="col-lg-12">
          
          <?php if($this->session->flashdata('success') != ""){?>
            <div class="alert alert-success">
          <?php echo $this->session->flashdata('success');?>
            </div>
          <?php }?>

          <?php if($this->session->flashdata('error') != ""){?>
            <div class="alert alert-danger">
          <?php echo $this->session->flashdata('error');?>
            </div>
          <?php }?>

            <div class="card">
                <div class="card-header">
                    <div class="card-title">
                        <form action="" method="get" name="searchForm" id="searchForm">
                            <div class="input-group mb-0">
                                <input type="text" name="query" id="query" class="form-control" placeholder="Search.." value="<?php echo $queryString;?>">
                                <div class="input-group-append">
                                    <button class="input-group-text" name="basic-addon1" id="basic-addon1">
                                    <i class="fas fa-search"></i>
                                    </button>
                                </div>
                            </div>
                        </form>
                    </div>
                    <div class="card-tools">
                        <a href="<?php echo base_url().'admin/category/create';?>" class="btn btn-primary"><i class="fas fa-plus"> Add Category</i></a>
                    </div>
                </div> 
                <div class="card-body">
                <table class="table">
                    <tr>
                        <th width="10%">#</th>
                        <th width="40%">Name</th>
                        <th width="20%">Status</th>
                        <th width="30%">Action</th>
                    </tr>
                    <?php if(!empty($categories)){
                     foreach($categories as $categoryRow){?>
                    <tr>
                        <td><?php echo $categoryRow['id'];?></td>
                        <td><?php echo $categoryRow['name'];?></td>
                        <td>
                          <?php if($categoryRow['status']==1){?>
                          <span class="badge badge-success">Active</span>
                          <?php } else{?>
                            <span class="badge badge-danger">InActive</span>
                            <?php }?>
                        </td>
                        <td><a href="<?php echo base_url().'admin/category/edit/'.$categoryRow['id']?>" class="btn btn-primary btn-sm"><i class="fas fa-edit"> Edit</i></a>
                        <a href="javascript:void(0)" onclick="deleteCategory(<?php echo $categoryRow['id'];?>)" class="btn btn-danger btn-sm"><i class="fas fa-trash"> Delete</i></a>
                        <a href="javascript:void(0)" onclick="updateCategoryStatus(<?php echo $categoryRow['id'];?>)" class="btn btn-warning btn-sm"><i class="fas fa-edit"> Status</i></a></td>
                    </tr>
                    <?php }
                   } else{ ?>
                      <tr>
                        <td colspan='4'>Categories Not Found!</td>
                      </tr>
                      <?php }?>
                </table>
            </div>   
            </div>
            
            
          </div>
          <!-- /.col-md-6 -->
        </div>
        <!-- /.row -->
      </div><!-- /.container-fluid -->
    </div>
    <!-- /.content -->
  </div>
  <!-- /.content-wrapper -->
<?php $this->load->view('admin/footer');?>

<script type="text/javascript">
  function deleteCategory(id){
    if(confirm("Are You Sure To Delete Category?")){
      window.location.href='<?php echo base_url().'admin/category/delete/';?>'+id;
    }
  }

  function updateCategoryStatus(id){
    if(confirm("Are You Sure To Update Category Status?")){
      window.location.href='<?php echo base_url().'admin/category/statusUpdate/';?>'+id;
    }
  }
</script>
<?php $this->load->view('admin/header');?>

  <!-- Content Wrapper. Contains page content -->
  <div class="content-wrapper">
    <!-- Content Header (Page header) -->
    <div class="content-header">
      <div class="container-fluid">
        <div class="row mb-2">
          <div class="col-sm-6">
            <h1 class="m-0 text-dark">Articles</h1>
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
                        <a href="<?php echo base_url().'admin/article/create';?>" class="btn btn-primary"><i class="fas fa-plus"> Add Article</i></a>
                    </div>
                </div> 
                <div class="card-body">
                <table class="table">
                    <tr>
                        <th width="5%">#</th>
                        <th width="10%">Image</th>
                        <th width="20%">Title</th>
                        <th width="15%">Author</th>
                        <th width="15%">Updated At</th>
                        <th width="10%">Status</th>
                        <th width="25%">Action</th>
                    </tr>
                    <?php if(!empty($articles)){
                     foreach($articles as $articleRow){?>
                    <tr>
                        <td><?php echo $articleRow['id'];?></td>
                        <td>
                        <?php 
                        $path = './public/uploads/article/thumb_admin/'.$articleRow['image'];
                        if($articleRow['image'] != "" && file_exists($path)){ ?>
                        <img class="w-100" src="<?php echo base_url('public/uploads/article/thumb_admin/'.$articleRow['image']);?>">
                        <?php 
                        } else {
                          ?>
                        <img class="w-100" src="<?php echo base_url().'public/uploads/article/no_image.jpg';?>">
                        <?php 
                        }
                        ?>
                        
                        
                        </td>
                        <td><?php echo substr($articleRow['title'],0,30);?></td>
                        <td><?php echo substr($articleRow['author'],0,20);?></td>
                        <td><?php $date =  new DateTime($articleRow['updated_at']); echo $date->format('d-m-Y');?></td>
                        <td>
                          <?php if($articleRow['status']==1){?>
                          <span class="badge badge-success">Active</span>
                          <?php } else{?>
                            <span class="badge badge-danger">InActive</span>
                            <?php }?>
                        </td>
                        <td><a href="<?php echo base_url().'admin/article/edit/'.$articleRow['id']?>" class="btn btn-primary btn-sm"><i class="fas fa-edit"> Edit</i></a>
                        <a href="javascript:void(0)" onclick="deleteArticle(<?php echo $articleRow['id'];?>)" class="btn btn-danger btn-sm"><i class="fas fa-trash"> Delete</i></a>
                        <a href="javascript:void(0)" onclick="updateArticleStatus(<?php echo $articleRow['id'];?>)" class="btn btn-warning btn-sm"><i class="fas fa-edit"> Status</i></a>
						</td>
                    </tr>
                    <?php }
                   } else{ ?>
                      <tr>
                        <td colspan='7'>Articles Not Found!</td>
                      </tr>
                      <?php }?>
                </table>
                <div>
                <?php echo $pagination_links?>
                </div>
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
  function deleteArticle(id){
    if(confirm("Are You Sure To Delete Article?")){
      window.location.href='<?php echo base_url().'admin/article/delete/';?>'+id;
    }
  }

  function updateArticleStatus(id){
    if(confirm("Are You Sure To Update Article Status?")){
      window.location.href='<?php echo base_url().'admin/article/statusUpdate/';?>'+id;
    }
  }
</script>
<?php $this->load->view('admin/header');?>
<!-- Content Wrapper. Contains page content -->
<div class="content-wrapper">
	<!-- Content Header (Page header) -->
	<div class="content-header">
		<div class="container-fluid">
			<div class="row mb-2">
				<div class="col-sm-6">
					<h1 class="m-0 text-dark">Articles</h1>
				</div>
				<!-- /.col -->
			</div>
			<!-- /.row -->
		</div>
		<!-- /.container-fluid -->
	</div>
	<!-- /.content-header -->
	<!-- Main content -->
	<div class="content">
		<div class="container-fluid">
			<div class="row">
				<div class="col-lg-12">
					<div class="card card-primary">
						<div class="card-header">
							<div class="card-title">
								Create New Article
							</div>
						</div>
						<form action="<?php echo base_url().'admin/article/create';?>" method="post" name="articleForm" id="articleForm" enctype="multipart/form-data">
							<div class="card-body">
                                <div class="form-group">
									<label for="name">Category</label>
									<select name="category_id" id="category_id" class="form-control <?php echo (form_error('category_id') != "") ? 'is-invalid' : '';?>">
                                    <option value="">Select A Category</option>
                                    <?php
                                    if(!empty($categories)){
                                        foreach($categories as $category){?>
                                            <option <?php echo set_select('category_id', $category['id'], false);?> value="<?php echo $category['id'];?>">
                                            <?php echo $category['name'];?>
                                            </option>
                                        <?php 
                                        }
                                    }
                                    ?>
                                    </select>
                                    <?php echo form_error('category_id');?>
								</div>
                                <div class="form-group">
									<label for="title">Title</label>
									<input type="text" name="title" id="title" class="form-control <?php echo (form_error('title') != "") ? 'is-invalid' : '';?>" value="<?php echo set_value('title');?>" placeholder="Article Title">
                                    <?php echo form_error('title');?>
                                </div>
                                <div class="form-group">
									<label for="description">Description</label>
                                    <textarea name="description" id="description" class="textarea"><?php echo set_value('description');?></textarea>
                                </div>
                                <div class="form-group">
									<label for="image">Article Image</label>
                                    <input type="file" name="image" id="image" class="form-control-file <?php echo (!empty($errorImageUpload)) ? 'is-invalid' : '';?>">
									<?php echo (!empty($errorImageUpload)) ? $errorImageUpload : '';?>
								</div>
                                <div class="form-group">
									<label for="author">Author</label>
									<input type="text" name="author" id="author" class="form-control <?php echo (form_error('author') != "") ? 'is-invalid' : '';?>" value="<?php echo set_value('author');?>" placeholder="Article Author">
                                    <?php echo form_error('author');?>
								</div>
								<div class="form-group">
									<div class="form-check custom-control custom-radio float-left">
										<input type="radio" class="custom-control-input" id="statusActive" name="status" value="1" checked>
										<label for="statusActive" class="custom-control-label">Active</label>
									</div>
									<div class="form-check custom-control custom-radio float-left ml-3">
										<input type="radio" class="custom-control-input" id="statusInactive" name="status" value="0">
										<label for="statusInactive" class="custom-control-label">Inactive</label>
									</div>
								</div>
							</div>
							<div class="card-footer">
								<button type="submit" class="btn btn-primary">Create</button>
								<a href="<?php echo base_url().'admin/article'?>" class="btn btn-secondary ml-3">Back</a>
							</div>
						</form>
					</div>
				</div>
			</div>
			<!-- /.col-md-6 -->
		</div>
		<!-- /.row -->
	</div>
	<!-- /.container-fluid -->
</div>
<!-- /.content -->
<!-- /.content-wrapper -->
<?php $this->load->view('admin/footer');?>
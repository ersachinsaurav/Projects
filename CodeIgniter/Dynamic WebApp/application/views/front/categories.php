<?php $this->load->view('front/header');?>

<!-- About -->
<div class="container pt-5 pb-5">
<h3 class="pb-4 pb-4">Categories</h3>
    <div class="row">
        <?php if(!empty($categories)){
            foreach($categories as $category){
                ?>
        <div class="col-md-4 pb-4 pt-4">
            <div class="card h-100">
                <a href="<?php echo base_url('blog/category/'.$category['id']);?>">
                <?php if(!empty($category['image']) && file_exists('./public/uploads/category/thumb/'.$category['image'])){?>
            <img src="<?php echo base_url('public/uploads/category/thumb/'.$category['image'])?>" class="card-img-top img-thumbnail">

          <?php }else{?>
            <img src="<?php echo base_url('public/uploads/category/no_image.jpg')?>" class="card-img-top img-thumbnail">
        <?php }?>
                </a>
                <div class="card-body">
                <a href="<?php echo base_url('blog/category/'.$category['id']);?>">
                <h5 class="card-title"><?php echo $category['name'];?></h5>
                </a>
                </div>
            </div>
        </div>
        <?php
		}
	}else{
        echo 'No Category Found!';
    }
	?>
	</div>
</div>

<?php $this->load->view('front/footer');?>
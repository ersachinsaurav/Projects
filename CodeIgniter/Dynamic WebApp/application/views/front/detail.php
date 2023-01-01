<?php $this->load->view('front/header');?>

<!-- About -->
<div class="container pt-4 pb-4">
<h3 class="pb-3">Blog</h3>
  <div class="row">
    <div class="col-md-12">
      <h3><?php echo $article['title'];?></h3>
      <div class="d-flex justify-content-between">
      <p class="text-muted">Posted By: <strong><?php echo $article['author']?></strong> on <strong><?php $date =  new DateTime($article['created_at']); echo $date->format('d-M-Y');?></strong></p>
      <a href="<?php echo base_url('blog/category/'.$article['category']);?>" class="text-muted p-2 bg-light text-uppercase"><strong><?php echo $article['category_name'];?></strong></a>
      </div>
      <div class="mb-3 mt-3">
      <?php if(!empty($article['image']) && file_exists('./public/uploads/article/thumb_front/'.$article['image'])){?>
            <img src="<?php echo base_url('public/uploads/article/thumb_front/'.$article['image'])?>" class="card-img-top img-thumbnail w-100">
          <?php }else{?>
            <img src="<?php echo base_url('public/uploads/article/no_image.jpg')?>" class="card-img-top img-thumbnail w-100">
      <?php }?>
      </div>
      <p><?php echo $article['description'];?></p>
      <div class="col-md-12 pl-0" id="comment_box">
      <?php 
      if(!empty(validation_errors())){
        ?>
        <div class="alert alert-danger">
          <h4 class="alert-heading">Please Fix The Following Errors !</h4>
          <?php echo validation_errors();?>
        </div>
      <?php
      }

      if(!empty($this->session->flashdata('message'))){
        ?>
        <div class="alert alert-success">
          <?php echo $this->session->flashdata('message');?>
        </div>
      <?php
      }
      ?>
      
        <div class="card">
        <div class="bg-light">
        <h4 class="text-center mt-1">Your Comments</h4>
        </div>
      <form action="<?php echo base_url().'blog/detail/'.$article['id'];?>#comment_box" method="post" name="commentForm" id="commentForm" enctype="multipart/form-data">
          <div class="card-body">
            <p>Comment</p>
            <div class="form-group">
              <textarea name="comment" id="comment" rows="2" class="form-control" placeholder="Comment.."><?php echo set_value('comment');?></textarea>
            </div>
            <div class="form-group">
            <label for="name">Your Name</label>
              <input type="text" name="name" id="name" class="form-control" placeholder="Your Name.." value="<?php echo set_value('name');?>">
            </div>
            <button type="submit" name="submit" class="btn btn-primary">Post</button>
		  </form>
          
        <div class="card-footer mt-4">
        <?php 
        if(!empty($comments)){
            foreach($comments as $comment){
                ?>
        <div class="user-comments">
            <p class="text-muted mt-3"><strong><?php echo $comment['name']?></strong></p>
            <p class="text-muted font-italic"><?php echo $comment['comment']?></p>
            <small class="text-muted">Posted On: <?php echo date('d-M-Y', strtotime($comment['created_at']))?></small>
            <hr>
        </div>
          <?php
          } 
        }else{?>
          <p class="text-muted font-italic text-center"><?php echo 'No Comments Found !';?></p>
        <?php 
        }
      ?>

        </div>
        </div>
        </div>
      </div>
	</div>
  </div>

</div>

<?php $this->load->view('front/footer');?>
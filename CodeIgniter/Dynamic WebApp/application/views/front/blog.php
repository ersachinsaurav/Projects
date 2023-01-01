<?php $this->load->view('front/header');?>

<div class="container">
    <h3 class="pt-4 pb-4">Blog</h3>

<?php if(!empty($articles)){
    foreach($articles as $article){
?>

    <div class="row pt-4 pd-4">
        <div class="col-md-4">
        <?php if(!empty($article['image']) && file_exists('./public/uploads/article/thumb_admin/'.$article['image'])){?>
            <img src="<?php echo base_url('public/uploads/article/thumb_admin/'.$article['image'])?>" class="card-img-top img-thumbnail">

          <?php }else{?>
            <img src="<?php echo base_url('public/uploads/article/no_image.jpg')?>" class="card-img-top img-thumbnail">
<?php }?>

        </div>        
        <div class="col-md-8">
            <p class="bg-light pt-2 pb-2 pl-3">
                <a href="<?php echo base_url('blog/category/'.$article['category']);?>" class="text-muted text-uppercase"><?php echo $article['category_name']?></a>
            </p>
            <h3>
            <a href="<?php echo base_url('blog/detail/'.$article['id']);?>"><?php echo word_limiter(strip_tags($article['title']), 35)?></a>
            </h3>
            <p><?php echo word_limiter(strip_tags($article['description']), 50)?>
            <a href="<?php echo base_url('blog/detail/'.$article['id']);?>" class="text-muted">Read More</a>
            </p>

            <p class="text-muted">Posted By: <strong><?php echo $article['author']?></strong> on <strong><?php $date =  new DateTime($article['created_at']); echo $date->format('d-M-Y');?></strong></p>
        </div>
    </div>
    <?php 
        }
    }else{
        echo 'No Blog Found!';
    }
    ?>
    <div class="row pt-5">
        <div class="col-md-12 align-right">
        <?php echo $pagination_links?>
        </div>
    </div>
</div>

<?php $this->load->view('front/footer');?>
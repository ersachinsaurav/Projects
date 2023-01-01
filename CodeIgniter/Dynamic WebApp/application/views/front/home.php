<?php $this->load->view('front/header');?>

<!-- Carousel -->
  <div id="carouselExampleControls" class="carousel slide carousel-fade" data-ride="carousel">
  <div class="carousel-inner">
    <div class="carousel-item active">
      <img src="<?php echo base_url('public/images/slide1.jpg')?>" class="d-block w-100">
    </div>
    <div class="carousel-item">
      <img src="<?php echo base_url('public/images/slide2.jpg')?>" class="d-block w-100">
    </div>
    <div class="carousel-item">
      <img src="<?php echo base_url('public/images/slide3.jpg')?>" class="d-block w-100">
    </div>
  </div>
  <a class="carousel-control-prev" href="#carouselExampleControls" role="button" data-slide="prev">
    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    <span class="sr-only">Previous</span>
  </a>
  <a class="carousel-control-next" href="#carouselExampleControls" role="button" data-slide="next">
    <span class="carousel-control-next-icon" aria-hidden="true"></span>
    <span class="sr-only">Next</span>
  </a>
</div>

<!-- About -->
<div class="container pt-4 pb-4">
<h3 class="pb-3">About Company</h3>
  <p class="text-muted">Lorem ipsum, dolor sit amet consectetur adipisicing elit. Dignissimos, numquam similique. Assumenda, perferendis in reprehenderit magnam odio provident et? Id accusantium fugiat quasi voluptatem. At dolor deserunt recusandae ab necessitatibus?</p>
  <p class="text-muted">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aut facere nihil corporis earum, quam, impedit aspernatur corrupti magnam laudantium, quae assumenda repellat modi ullam atque placeat explicabo eveniet. Voluptas nostrum maxime perferendis praesentium recusandae laborum ipsam vitae minus ipsa voluptatibus, laudantium consequatur illum officiis libero cumque exercitationem quidem, nobis sit veritatis velit quasi illo cupiditate. Modi error minima tempore eaque aspernatur aperiam ipsa, sequi sapiente, dolor nemo obcaecati libero ratione totam. Sapiente praesentium voluptate voluptates.</p>
</div>

<!-- Services -->
<div class="bg-light pb-4">
	<div class="container">
		<h3 class="pb-4 pt-4">Our Services</h3>
		<div class="row">
			<div class="col-md-3">
				<div class="card h-100">
					<img src="<?php echo base_url('public/images/box1.jpg')?>" class="card-img-top">
					<div class="card-body">
						<h5 class="card-title">Website Development</h5>
						<p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
					</div>
				</div>
			</div>
			<div class="col-md-3">
				<div class="card h-100">
					<img src="<?php echo base_url('public/images/box2.jpg')?>" class="card-img-top">
					<div class="card-body">
						<h5 class="card-title">Software Development</h5>
						<p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
					</div>
				</div>
			</div>
			<div class="col-md-3">
				<div class="card h-100">
					<img src="<?php echo base_url('public/images/box3.jpg')?>" class="card-img-top">
					<div class="card-body">
						<h5 class="card-title">Mobile App Development</h5>
						<p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
					</div>
				</div>
			</div>
			<div class="col-md-3">
				<div class="card h-100">
					<img src="<?php echo base_url('public/images/box4.jpg')?>" class="card-img-top">
					<div class="card-body">
						<h5 class="card-title">UI/UX Designing</h5>
						<p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>

<?php 
if(!empty($articles)){
?>
<!-- Blogs -->
<div class="pb-4">
	<div class="container">
		<h3 class="pb-4 pt-4">Latest Blogs</h3>
		<div class="row">
    <?php foreach($articles as $article){?>
			<div class="col-md-3">
				<div class="card h-100">
			<a href="<?php echo base_url('blog/detail/'.$article['id']);?>">
          <?php if(!empty($article['image']) && file_exists('./public/uploads/article/thumb_admin/'.$article['image'])){?>
            <img src="<?php echo base_url('public/uploads/article/thumb_admin/'.$article['image'])?>" class="card-img-top">

          <?php }else{?>
            <img src="<?php echo base_url('public/uploads/article/no_image.jpg')?>" class="card-img-top">
<?php }?>
</a>
					<div class="card-body">
					<a href="<?php echo base_url('blog/detail/'.$article['id']);?>">
						<p class="card-text"><?php echo $article['title'];?></p>
						</a>
					</div>
				</div>
			</div>
    <?php }?>
		</div>
	</div>
</div>

<?php
}
$this->load->view('front/footer');?>
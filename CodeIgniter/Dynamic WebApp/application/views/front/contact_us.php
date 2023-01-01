<?php $this->load->view('front/header');?>
<div class="container-fluid" style="background-image:url(../public/images/ball-bright-close-up-clouds-207489.jpg);">
<div class="row">
    <div class="col-md-12 pt-5">
    <h1 class="text-center text-white">Contact Us</h1>
    </div>
    <div class="container pt-5">
        <div class="row mb-5">
            <div class="col-md-7">
                <div class="card h-100">
                    <div class="card-header bg-secondary text-white">
                    Have Questions Or Comments?
                    </div>
                    <div class="card-body">
                    <?php if(!empty($this->session->flashdata('msg'))){
                        ?>
                        <div class="alert alert-success">
                        <?php echo $this->session->flashdata('msg');?>
                        </div>
                    <?php
                 }
                ?>
                        <form action="<?php echo base_url('page/contact');?>" method="post" name="contactForm" id="contactForm">
                            
                            <div class="form-group">
                            <label for="name">Name</label>
                            <input type="text" name="name" id="name" class="form-control <?php echo (form_error('name') != "") ? 'is-invalid' : '';?>" placeholder="Your Name.." value="<?php echo set_value('name');?>">
                            <?php echo form_error('name');?>
                            </div>
                            
                            <div class="form-group">
                            <label for="email">Email</label>
                            <input type="text" name="email" id="email" class="form-control <?php echo (form_error('email') != "") ? 'is-invalid' : '';?>" placeholder="Your Email.." value="<?php echo set_value('email');?>">
                            <?php echo form_error('email');?>
                            </div>
                            
                            <div class="form-group">
                            <label for="name">Message</label>
                            <textarea name="message" id="message" rows="5" class="form-control" placeholder="Your Message.."><?php echo set_value('message');?></textarea>
                            </div>
                            <button type="submit" name="submit" id="submit" class="btn btn-primary">Send</button>
                        </form>
                    </div>
                </div>            
            </div>
            <div class="col-md-5">
                <div class="card h-100">
                    <div class="card-header bg-secondary text-white">
                        Reach Us
                    </div>
                    <div class="card-body">
                        <p class="font-weight-bold mb-0">Customer Service:</p>
                        <p class="mb-0">Phone: 1800 000 1060</p>
                        <p>Email: support@enspyrme.com</p>

                        <p class="font-weight-bold mb-0">Head Quarter:</p>
                        <p class="mb-0">Surya Complex, Laxmi Chowk,</p>
                        <p class="mb-0">Muzaffarpur, Bihar - 842003 (IN)</p>
                        <p class="mb-0">Phone: 1800 000 1060</p>
                        <p>Email: support@enspyrme.com</p>

                        <p class="font-weight-bold mb-0">Head Quarter:</p>
                        <p class="mb-0">Surya Complex, Laxmi Chowk,</p>
                        <p class="mb-0">Muzaffarpur, Bihar - 842003 (IN)</p>
                        <p class="mb-0">Phone: 1800 000 1060</p>
                        <p>Email: support@enspyrme.com</p>

                    </div>
                </div>
            </div>
        </div>
    </div>
    
</div>

</div>
<?php $this->load->view('front/footer');?>
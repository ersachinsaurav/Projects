<?php
defined('BASEPATH') OR exit('No direct script access allowed');

class Article extends CI_Controller {

	public function __construct(){
		parent::__construct();
		$admin = $this->session->userdata('admin');
		if(empty($admin)){
			$this->session->set_flashdata('msg', 'Session Expired!');
			redirect(base_url().'admin/login');
		}

	}

	public function index($page=1)
	{
		$this->load->model("Article_model");
		$this->load->library("pagination");

		$data['mainModule'] = 'article';
		$data['subModule'] = 'viewArticle';
	
		$config['reuse_query_string'] = TRUE;
		$config['per_page'] = 5;
		$param['offset'] = $config['per_page'];
		$param['limit'] = ($page * $config['per_page']) - $config['per_page'];
		$param['queryString'] = $this->input->get('query');
		
		$config['base_url'] = base_url('admin/article/index');
		$config['total_rows'] = $this->Article_model->getArticlesCount($param);
		$config['use_page_numbers'] = true;
		
		//BootStrap Pagination Style
		$config['next_link'] = 'Next';
		$config['prev_link'] = 'Prev';
		$config['full_tag_open'] = "<ul class='pagination'>";
		$config['full_tag_close'] = "</ul>";
		$config['num_tag_open'] = "<li class='page-item'>";
		$config['num_tag_close'] = "</li>";
		$config['cur_tag_open'] = "<li class='disabled page-item'><li class='active page-item'><a href='#' class='page-link'>";
		$config['cur_tag_close'] = "<span class='sr-only'></span></a></li>";
		$config['next_tag_open'] = "<li class='page-item'>";
		$config['next_tag_close'] = "</li>";
		$config['prev_tag_open'] = "<li class='page-item'>";
		$config['prev_tag_close'] = "</li>";
		$config['first_tag_open'] = "<li class='page-item'>";
		$config['first_tag_close'] = "</li>";
		$config['last_tag_open'] = "<li class='page-item'>";
		$config['last_tag_close'] = "</li>";
		$config['attributes'] = array('class' => 'page-link');

		$this->pagination->initialize($config);
		$pagination_links = $this->pagination->create_links();
		$articles = $this->Article_model->getArticles($param);
		$data['articles'] = $articles;
		$data['queryString'] = $param['queryString'];
		$data['pagination_links'] = $pagination_links;
		$this->load->view("admin/article/list", $data);
	}

    public function create()
	{
		$this->load->model("Category_model");
		$this->load->model("Article_model");
		$this->load->helper('common');
		$this->load->library('form_validation');
		$categories = $this->Category_model->getCategoriesArticles();
		$data['categories'] = $categories;
	
		$data['mainModule'] = 'article';
		$data['subModule'] = 'createArticle';
		
		//image upload setting
		$config['upload_path'] = './public/uploads/article/';
		$config['allowed_types'] = "gif|png|jpg|jpeg";
		$config['encrypt_name'] = true;
		$this->load->library('upload', $config);

		$this->form_validation->set_error_delimiters('<p class="invalid-feedback">', '</p>');
		$this->form_validation->set_rules('category_id', 'Category', 'trim|required');
		$this->form_validation->set_rules('title', 'Article Title', 'trim|required|min_length[20]');
		$this->form_validation->set_rules('author', 'Author Name', 'trim|required');

		if($this->form_validation->run()){
			if(!empty($_FILES['image']['name'])){

				if($this->upload->do_upload('image')){

					$data = $this->upload->data();

					resizeImage($config['upload_path'].$data['file_name'], $config['upload_path'].'thumb_admin/'.$data['file_name'],300, 270);
					resizeImage($config['upload_path'].$data['file_name'], $config['upload_path'].'thumb_front/'.$data['file_name'],1120, 800);
					
					$formArray['image'] = $data['file_name'];
					$formArray['title'] = $this->input->post('title');
					$formArray['category'] = $this->input->post('category_id');
					$formArray['description'] = $this->input->post('description');
					$formArray['author'] = $this->input->post('author');
					$formArray['status'] = $this->input->post('status');
					date_default_timezone_set('Asia/Kolkata'); 
					$formArray['created_at'] = date('Y-m-d H:i:s');
					$this->Article_model->addArticle($formArray);

					$this->session->set_flashdata('success', 'Article Added Successfully!');
					redirect(base_url().'admin/article');

					
				}else{
					$error = $this->upload->display_errors('<p class="invalid-feedback">','</p>');
					$data['errorImageUpload'] = $error;
					$this->load->view('admin/article/create', $data);
				}
			}else{
				//without image
				$formArray['title'] = $this->input->post('title');
				$formArray['category'] = $this->input->post('category_id');
				$formArray['description'] = $this->input->post('description');
				$formArray['author'] = $this->input->post('author');
				$formArray['status'] = $this->input->post('status');
				date_default_timezone_set('Asia/Kolkata'); 
				$formArray['created_at'] = date('Y-m-d H:i:s');
				$this->Article_model->addArticle($formArray);

				$this->session->set_flashdata('success', 'Article Added Successfully!');
				redirect(base_url().'admin/article');
			}

		}else{
			$this->load->view("admin/article/create", $data);
		}
	}

	public function edit($id)
	{
		$this->load->library('form_validation');
		$this->load->model('Article_model');
		$this->load->model('Category_model');
		$this->load->helper('common');
		
		$data['mainModule'] = 'article';
		$data['subModule'] = 'editArticle';

		$article = $this->Article_model->getArticle($id);

		if(empty($article)){
			$this->session->set_flashdata('error', 'Article Not Found !');
			redirect(base_url().'admin/article');
		}
		$categories = $this->Category_model->getCategoriesArticles();
		$data['categories'] = $categories;
		$data['article'] = $article;

		//image upload setting
		$config['upload_path'] = './public/uploads/article/';
		$config['allowed_types'] = "gif|png|jpg|jpeg";
		$config['encrypt_name'] = true;
		$this->load->library('upload', $config);

		$this->form_validation->set_error_delimiters('<p class="invalid-feedback">', '</p>');
		$this->form_validation->set_rules('category_id', 'Category', 'trim|required');
		$this->form_validation->set_rules('title', 'Article Title', 'trim|required|min_length[20]');
		$this->form_validation->set_rules('author', 'Author Name', 'trim|required');

		if($this->form_validation->run()){
			if(!empty($_FILES['image']['name'])){

				if($this->upload->do_upload('image')){

					$data = $this->upload->data();

					resizeImage($config['upload_path'].$data['file_name'], $config['upload_path'].'thumb_admin/'.$data['file_name'],300, 270);
					resizeImage($config['upload_path'].$data['file_name'], $config['upload_path'].'thumb_front/'.$data['file_name'],1120, 800);
					
					$formArray['image'] = $data['file_name'];
					$formArray['title'] = $this->input->post('title');
					$formArray['category'] = $this->input->post('category_id');
					$formArray['description'] = $this->input->post('description');
					$formArray['author'] = $this->input->post('author');
					$formArray['status'] = $this->input->post('status');
					date_default_timezone_set('Asia/Kolkata'); 
					$formArray['updated_at'] = date('Y-m-d H:i:s');
					$this->Article_model->updateArticle($id, $formArray);

					//deleting old images
					if(file_exists('./public/uploads/article/thumb_admin/'.$article['image'])){
						unlink('./public/uploads/article/thumb_admin/'.$article['image']);
					}
			
					if(file_exists('./public/uploads/article/thumb_front/'.$article['image'])){
						unlink('./public/uploads/article/thumb_front/'.$article['image']);
					}
			
					if(file_exists('./public/uploads/article/'.$article['image'])){
						unlink('./public/uploads/article/'.$article['image']);
					}

					$this->session->set_flashdata('success', 'Article Updated Successfully!');
					redirect(base_url().'admin/article');

					
				}else{
					$error = $this->upload->display_errors('<p class="invalid-feedback">','</p>');
					$data['errorImageUpload'] = $error;
					$this->load->view("admin/article/edit", $data);
				}
			}else{
				//without image
				$formArray['title'] = $this->input->post('title');
				$formArray['category'] = $this->input->post('category_id');
				$formArray['description'] = $this->input->post('description');
				$formArray['author'] = $this->input->post('author');
				$formArray['status'] = $this->input->post('status');
				date_default_timezone_set('Asia/Kolkata'); 
				$formArray['updated_at'] = date('Y-m-d H:i:s');
				$this->Article_model->updateArticle($id, $formArray);

				$this->session->set_flashdata('success', 'Article Updated Successfully!');
				redirect(base_url().'admin/article');
			}

		}else{
			$this->load->view("admin/article/edit", $data);
		}
	}

	public function delete($id)
	{
		$this->load->model('Article_model');
		$article = $this->Article_model->getArticle($id);
		
		if(empty($article)){
			$this->session->set_flashdata('error', 'Article Not Found !');
			redirect(base_url().'admin/article');
		}

		if(file_exists('./public/uploads/article/thumb_admin/'.$article['image'])){
			unlink('./public/uploads/article/thumb_admin/'.$article['image']);
		}

		if(file_exists('./public/uploads/article/thumb_front/'.$article['image'])){
			unlink('./public/uploads/article/thumb_front/'.$article['image']);
		}

		if(file_exists('./public/uploads/article/'.$article['image'])){
			unlink('./public/uploads/article/'.$article['image']);
		}

		$article = $this->Article_model->deleteArticle($id);
		$this->session->set_flashdata('success', 'Article Deleted Successfully !');
		redirect(base_url().'admin/article');
	}

	public function statusUpdate($id)
	{
		$this->load->model('Article_model');
		$article = $this->Article_model->getArticle($id);
		
		if(empty($article)){
			$this->session->set_flashdata('error', 'Article Not Found !');
			redirect(base_url().'admin/article');
		}

		$articleStatus = $article['status'];
		if($articleStatus == 1 ){
			$articleStatus = 0;
		}else{
			$articleStatus = 1;
		}

		$article = $this->Article_model->statusUpdate($id, $articleStatus);
		$this->session->set_flashdata('success', 'Article Status Updated Successfully !');
		redirect(base_url().'admin/article');
	}
}
<?php
defined('BASEPATH') OR exit('No direct script access allowed');

class Blog extends CI_Controller {

	public function index($page = 1)
	{
        $this->load->library("pagination");
        $this->load->helper('text');
        $this->load->model('Article_model');
        
		//$config['reuse_query_string'] = TRUE;
		$config['per_page'] = 5;
		$param['offset'] = $config['per_page'];
		$param['limit'] = ($page * $config['per_page']) - $config['per_page'];
		
		$config['base_url'] = base_url('blog/index');
		$config['total_rows'] = $this->Article_model->getArticlesCountFront();
		$config['use_page_numbers'] = true;
		
		//BootStrap Pagination Style
		$config['next_link'] = 'Next';
		$config['prev_link'] = 'Prev';
		$config['full_tag_open'] = "<ul class='pagination justify-content-center'>";
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
		
        $data['pagination_links'] = $pagination_links;
		        
        $articles = $this->Article_model->getArticlesFront($param);
        $data['articles'] = $articles;

        $this->load->view('front/blog', $data);
    }

    public function categories(){
        $this->load->model('Category_model');
        $categories = $this->Category_model->getCategoriesFront();
        $data['categories'] = $categories;
        $this->load->view('front/categories', $data);
    }

    public function detail($id = 1){
        $this->load->model('Article_model');
        $this->load->model('Comment_model');
        $this->load->library('form_validation');
        
		$article = $this->Article_model->getArticleFront($id);
		if(empty($article)){
			redirect(base_url('blog'));
		}
        $data['article'] = $article;

		$comments = $this->Comment_model->getComments($id, true);
        $data['comments'] = $comments;
		
		$this->form_validation->set_rules('name', 'Name', 'required|min_length[3]');
		$this->form_validation->set_rules('comment', 'Comment', 'required|min_length[20]');
		$this->form_validation->set_error_delimiters('<p class="mb-0">', '</p>');

		if($this->form_validation->run()){
			$formArray['name'] = $this->input->post('name');
			$formArray['comment'] = $this->input->post('comment');
			$formArray['article_id'] = $id;

			$this->Comment_model->insert($formArray);
			$this->session->set_flashdata('message', 'Your Comment Has Been Posted Successfully!');
			redirect(base_url('blog/detail/'.$id.'#comment_box'));
		}else{

			$this->load->view('front/detail', $data);
		}

    }

	public function category($category_id=1, $page=1){
		$this->load->library("pagination");
        $this->load->helper('text');
        $this->load->model('Article_model');
        $this->load->model('Category_model');
        $category = $this->Category_model->getCategory($category_id);
		
		//$config['reuse_query_string'] = TRUE;
		$config['per_page'] = 5;
		$param['offset'] = $config['per_page'];
		$param['limit'] = ($page * $config['per_page']) - $config['per_page'];
		$param['category_id'] = $category_id;
		
		$config['base_url'] = base_url('blog/category/'.$category_id);
		$config['total_rows'] = $this->Article_model->getArticlesCountFront($param);
		$config['uri_segment'] = 4;
		$config['use_page_numbers'] = true;
		
		//BootStrap Pagination Style
		$config['next_link'] = 'Next';
		$config['prev_link'] = 'Prev';
		$config['full_tag_open'] = "<ul class='pagination justify-content-center'>";
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
		
        $data['pagination_links'] = $pagination_links;
		        
        $articles = $this->Article_model->getArticlesFront($param);
        $data['articles'] = $articles;
        $data['category'] = $category;

		$this->load->view('front/category_articles', $data);	
	}
}
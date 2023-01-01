<?php
defined('BASEPATH') OR exit('No direct script access allowed');

class Login extends CI_Controller {

	public function index()
	{
		$admin = $this->session->userdata('admin');
		if(!empty($admin)){
			redirect(base_url().'admin/home');
		}
		$this->load->library('form_validation');
		$this->load->view('admin/login');
	}

	public function authenticate()
	{
		$this->load->library('form_validation');
		$this->load->model('Admin_model');

		$this->form_validation->set_rules('username', 'Username', 'trim|required');
		$this->form_validation->set_rules('password', 'Password', 'required');

		if($this->form_validation->run()){
			//Field Not Empty
			$username = $this->input->post('username');
			$admin = $this->Admin_model->getByUsername($username);
			if(!empty($admin)){
				$password = $this->input->post('password');
				if(password_verify($password, $admin['password'])){
					$adminArray['admin_id'] = $admin['id'];
					$adminArray['username'] = $admin['username'];
					$this->session->set_userdata('admin', $adminArray);
					redirect(base_url().'admin/home');
				}else{
					//Password Error
					$this->session->set_flashdata('msg', 'Either Username Or Password Is Incorrect!');
					redirect(base_url().'admin/login');
				}	
			}else{
				//Username Error
				$this->session->set_flashdata('msg', 'Either Username Or Password Is Incorrect!');
				redirect(base_url().'admin/login');
			}
		}else{
			//Empty Field
			$this->session->set_flashdata('msg', 'Username And Password Is Required!');
			redirect(base_url().'admin/login');
		}
	}
	function logout(){
		$this->session->unset_userdata('admin');
		redirect(base_url().'admin/login');
	}

}
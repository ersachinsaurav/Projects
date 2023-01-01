<?php
defined('BASEPATH') OR exit('No direct script access allowed');

class Page extends CI_Controller {

	public function about()
	{
        $this->load->view('front/about');
    }

    public function services()
	{
        $this->load->view('front/services');
    }

    public function contact()
	{
        $this->load->library('form_validation');
        $this->form_validation->set_rules('name', 'Name', 'required|min_length[3]');
        $this->form_validation->set_rules('email', 'Email', 'required|valid_email');
        $this->form_validation->set_error_delimiters('<p class="invalid-feedback">', '</p>');

        if($this->form_validation->run()){
            $config = Array(
            'protocol' => 'smtp',
            'smtp_host' => 'ssl://smtp.gmail.com',
            'smtp_port' => 465,
            'smtp_user' => 'sachin.saurav367@gmail.com',
            'smtp_pass' => '205975179311',
            'mailtype' => 'html',
            'charset' => 'iso-8859-1',
            );
            $this->load->library('email', $config);
            $this->email->set_newline("\r\n");

            $this->email->to('sauravicafe@gmail.com');
            $this->email->from('no-reply@enspyrme.com');
            $this->email->subject('You Have Recieved New Enquiry');
            $name = $this->input->post('name');
            $email = $this->input->post('email');
            $msg = $this->input->post('message');
            

            $message = "Name: ".$name;
            $message .= "<br>";
            $message .= "Email: ".$email;
            $message .= "<br>";
            $message .= "Message: ".$msg;
            $message .= "<br>";
            $message .= "<br>";
            $message .= "With Regards!";
            
            $this->email->message($message);
            $this->email->send();
            $this->session->set_flashdata('msg', 'Thank You For Your Enquiry, We Will Get Back To You Soon!');
            redirect(base_url('page/contact'));        
        }else{
            $this->load->view('front/contact_us');
        }
    }
}
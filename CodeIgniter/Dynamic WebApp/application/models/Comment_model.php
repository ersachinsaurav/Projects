<?php
defined('BASEPATH') OR exit('No direct script access allowed');

class Comment_model extends CI_Model {

	public function insert($formArray)
	{
		$this->db->insert('comments', $formArray);
    }

    public function getComments($article_id, $status = null)
	{
		$this->db->where('article_id', $article_id);
        if($status){
            $this->db->where('status', 1);
        }
        $this->db->order_by('created_at', 'DESC');
        $comments = $this->db->get('comments')->result_array();
        return $comments;
    }
}
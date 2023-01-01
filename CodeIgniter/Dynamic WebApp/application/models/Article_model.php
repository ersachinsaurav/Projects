<?php
defined('BASEPATH') OR exit('No direct script access allowed');

class Article_model extends CI_Model {

	public function addArticle($formArray)
	{
		$this->db->insert('articles', $formArray);
		return $this->db->insert_id();
	}

	//method to list articles
	public function getArticles($param = array()){
		if(isset($param['offset']) && isset($param['limit'])){
			$this->db->limit($param['offset'], $param['limit']);
		}

		if(isset($param['queryString'])){
			$this->db->or_like('title', trim($param['queryString']));
			$this->db->or_like('author', trim($param['queryString']));
		}

		$query = $this->db->get('articles');
		$articles = $query->result_array();
		return $articles;
	}

	public function getArticlesCount($param = array()){
		if(isset($param['queryString'])){
			$this->db->or_like('title', trim($param['queryString']));
			$this->db->or_like('author', trim($param['queryString']));
		}
		
		$count = $this->db->count_all_results('articles');
		return $count;
	}

	public function getArticle($id){
		$this->db->where('id', $id);
		$article = $this->db->get('articles')->row_array();
		return $article; 
	}

	public function updateArticle($id, $formArray){
		$this->db->where('id', $id);
		$this->db->update('articles', $formArray);
	}

	public function deleteArticle($id){
		 $this->db->where('id', $id);
		 $this->db->delete('articles');
	}

	public function statusUpdate($id, $articleStatus){
		$status = array('status' => $articleStatus);    
		$this->db->where('id', $id);
		$this->db->update('articles', $status);
   }

	//Front End Methods
	public function getArticlesFront($param = array()){
		if(isset($param['offset']) && isset($param['limit'])){
			$this->db->limit($param['offset'], $param['limit']);
		}

		if(isset($param['category_id'])){
			$this->db->where('category', $param['category_id']);
		}
		
		$this->db->select('articles.*, categories.name as category_name');
		$this->db->where('articles.status', 1);
		$this->db->order_by('articles.created_at', 'DESC');

		$this->db->join('categories', 'categories.id = articles.category', 'left');
		
		$query = $this->db->get('articles');
		$articles = $query->result_array();
		return $articles;
	}

	public function getArticlesCountFront($param = array()){
		$this->db->where('articles.status', 1);

		if(isset($param['category_id'])){
			$this->db->where('category', $param['category_id']);
		}

		$count = $this->db->count_all_results('articles');
		return $count;
		echo $this->db->last_query();
	}

	public function getArticleFront($id){
		$this->db->select('articles.*, categories.name as category_name');
		$this->db->where('articles.id', $id);
		$this->db->join('categories', 'categories.id = articles.category', 'left');
		$article = $this->db->get('articles')->row_array();
		return $article; 
	}

}
<!DOCTYPE html>
<!--
	This is a starter template page. Use this page to start your new project from
	scratch. This page gets rid of all links and provides the needed markup only.
	-->
<html lang="en">
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<meta http-equiv="x-ua-compatible" content="ie=edge">
		<title>Admin Panel</title>
		<!-- Font Awesome Icons -->
		<link rel="stylesheet" href="<?php echo base_url()?>public/admin/plugins/fontawesome-free/css/all.min.css">
		<!-- Theme style -->
		<link rel="stylesheet" href="<?php echo base_url()?>public/admin/dist/css/adminlte.min.css">
		<!-- Text Editor -->
		<link rel="stylesheet" href="<?php echo base_url()?>public/admin/plugins/summernote/summernote-bs4.css">
		<!-- Google Font: Source Sans Pro-->
		<link rel="stylesheet" href="<?php echo base_url()?>public/admin/dist/css/sourcesanspro.css">
		
		</head>
	<body class="hold-transition sidebar-mini">
		<div class="wrapper">
		<!-- Navbar -->
		<nav class="main-header navbar navbar-expand navbar-white navbar-light">
			<ul class="navbar-nav">
				<li class="nav-item">
					<a class="nav-link" data-widget="pushmenu" href="#" role="button"><i class="fas fa-bars"></i></a>
				</li>
			</ul>
			<!-- Right navbar links -->
			<ul class="navbar-nav ml-auto">
				<!-- Notifications Dropdown Menu -->
				<li class="nav-item dropdown">
					<a class="nav-link" data-toggle="dropdown" href="#">
					Welcome, <strong>Administrator</strong></a>
					<div class="dropdown-menu dropdown-menu-lg dropdown-menu-right">
						<div class="dropdown-divider"></div>
						<a href="<?php echo base_url().'admin/login/logout'?>" class="dropdown-item">
						Logout
						</a>
					</div>
				</li>
			</ul>
		</nav>
		<!-- /.navbar -->
		<!-- Main Sidebar Container -->
		<aside class="main-sidebar sidebar-dark-primary elevation-4">
			<!-- Brand Logo -->
			<a href="" class="brand-link">
			<img src="<?php echo base_url()?>public/admin/dist/img/AdminLTELogo.png" alt="AdminLTE Logo" class="brand-image img-circle elevation-3"
				style="opacity: .8">
			<span class="brand-text font-weight-bold">CI Admin Panel</span>
			</a>
			<!-- Sidebar -->
			<div class="sidebar">
				<!-- Sidebar user panel (optional) -->
				<div class="user-panel mt-3 pb-3 mb-3 d-flex">
					<div class="image">
						<img src="<?php echo base_url()?>public/admin/dist/img/user2-160x160.jpg" class="img-circle elevation-2" alt="User Image">
					</div>
					<div class="info">
						<a href="#" class="d-block">Sachin Saurav</a>
					</div>
				</div>
				<!-- Sidebar Menu -->
				<nav class="mt-2">
					<ul class="nav nav-pills nav-sidebar flex-column" data-widget="treeview" role="menu" data-accordion="false">
						<!-- Add icons to the links using the .nav-icon class
							with font-awesome or any other icon font library -->
						<li class="nav-item has-treeview <?php echo (!empty ($mainModule) && $mainModule == 'category') ? 'menu-open' : ''?>">
							<a href="#" class="nav-link <?php echo (!empty ($mainModule) && $mainModule == 'category') ? 'active' : ''?>">
								<i class="nav-icon fas fa-tachometer-alt"></i>
								<p>
									Categories
									<i class="right fas fa-angle-left"></i>
								</p>
							</a>
							<ul class="nav nav-treeview">
								<li class="nav-item">
									<a href="<?php echo base_url().'admin/category/create'?>" class="nav-link <?php echo (!empty ($mainModule) && $mainModule == 'category' && !empty ($subModule) && $subModule == 'createCategory') ? 'active' : ''?>">
										<i class="far fa-circle nav-icon"></i>
										<p>Add Categories</p>
									</a>
								</li>
								<li class="nav-item">
									<a href="<?php echo base_url().'admin/category'?>" class="nav-link <?php echo (!empty ($mainModule) && $mainModule == 'category' && !empty ($subModule) && $subModule == 'viewCategory') ? 'active' : ''?>">
										<i class="far fa-circle nav-icon"></i>
										<p>View Categories</p>
									</a>
								</li>
							</ul>
						</li>
						<li class="nav-item has-treeview <?php echo (!empty ($mainModule) && $mainModule == 'article') ? 'menu-open' : ''?>">
							<a href="#" class="nav-link <?php echo (!empty ($mainModule) && $mainModule == 'article') ? 'active' : ''?>">
								<i class="nav-icon fas fa-tachometer-alt"></i>
								<p>
									Articles
									<i class="right fas fa-angle-left"></i>
								</p>
							</a>
							<ul class="nav nav-treeview">
								<li class="nav-item">
									<a href="<?php echo base_url().'admin/article/create'?>" class="nav-link <?php echo (!empty ($mainModule) && $mainModule == 'article' && !empty ($subModule) && $subModule == 'createArticle') ? 'active' : ''?>">
										<i class="far fa-circle nav-icon"></i>
										<p>Add Article</p>
									</a>
								</li>
								<li class="nav-item">
									<a href="<?php echo base_url().'admin/article'?>" class="nav-link <?php echo (!empty ($mainModule) && $mainModule == 'article' && !empty ($subModule) && $subModule == 'viewArticle') ? 'active' : ''?>">
										<i class="far fa-circle nav-icon"></i>
										<p>View Article</p>
									</a>
								</li>
							</ul>
						</li>
						<li class="nav-item">
							<a href="<?php echo base_url().'admin/login/logout'?>" class="nav-link">
								<i class="nav-icon fas fa-th"></i>
								<p>
									Logout
								</p>
							</a>
						</li>
					</ul>
				</nav>
				<!-- /.sidebar-menu -->
			</div>
			<!-- /.sidebar -->
		</aside>
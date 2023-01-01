function Del(id){
	if (confirm("Do you want to Delete this record?")) {
		$.ajax({
			url: "delete.php",
			type: "post",
			data: {
				"delete": 1,
				"id": id,
			},
			success: function (response) {
				if (response == "true") {
					$("#data").load("data.php");
					alert("Deleted!");
				} else {
					alert(response);
				}
			}
		});
	}
}

function Edit(id){
	$.ajax({
		url: "formUpdate.php",
		type: "POST",
		data: {
			id: id
		},
		cache: false,
		success: function (result) {
			$("#form").html(result);
		}
	});
	$("html, body").animate({ scrollTop: 0 }, "slow");
}
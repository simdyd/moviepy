function mostra_elenco_film_spalla(object_id,tipo){
	$.ajax({
	type: "GET",
	url: "/ws/get_movie_list_spalla/",
	data: "objectid="+object_id+"&tipo="+tipo,
	success: function(msg){
	$("#spalla_dx").html(msg);
	}
	});

	}
	
	function mostra_detail_film_spalla(film_id){
	$.ajax({
	type: "GET",
	url: "/ws/get_movie_detail/",
	data: "filmid="+film_id,
	success: function(msg){
	$("#spalla_dx").html(msg);
	}
	});

	}
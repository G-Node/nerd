map = function() {
	var i = this._id;
	var id = this.object_id;

	if (this.isLatest == true) {
		this.properties.forEach(
			function(z) { 
				if (z.name == property_name) {
					var checkValue = false;
					z.values.forEach(  
						function(x) {
							if (x.value == value_name) {
								checkValue = true;
							}
						}
					);
	
					if (checkValue) {
						emit(i, id);
					}
				} 
			} 
		);
	}
}

reduce = function(key, value) {
	return value;
}